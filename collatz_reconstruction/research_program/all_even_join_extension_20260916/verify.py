#!/usr/bin/env python3
"""Exact all-even-template tests; counts are individual checked identities."""
from pathlib import Path
import argparse, hashlib, json, math
import all_even as a

COUNTS={}
def check(kind,ok):
    if not ok:raise a.old.CertificateError(kind)
    COUNTS[kind]=COUNTS.get(kind,0)+1

def affine_leg(n0,ns,word):
    rows=[]
    for e in word:
        check('affine_constant_division',(3*n0+1)%(1<<e)==0)
        check('affine_slope_division',(3*ns)%(1<<e)==0)
        n0,ns=(3*n0+1)//(1<<e),3*ns//(1<<e)
        check('exact_odd_endpoint',n0>0 and n0%2==1 and ns%2==0)
        rows.append([n0,ns])
    return n0,ns,rows

def negative(f):
    try:f()
    except (ValueError,TypeError):return True
    return False

def run():
    for e in range(2,514,2):
        h,t,u=a.interior_data(e)
        check('interior_identity',3*h==(1<<e)+2 and h%4==2 and u%3!=0)
    family_rows=[]
    for b in range(1,17):
        for e in range(2,34,2):
            for side in (False,True):
                f=a.family(b,e,side)
                x,xs,l=affine_leg(f['n0'],f['nstep'],f['left_word'])
                y,ys,r=affine_leg(f['m0'],f['mstep'],f['right_word'])
                check('full_family_target',(x,xs)==(y,ys)==(f['y0'],f['ystep']))
                check('whole_height_interval',f['height_constant']>0 and f['height_slope']>0)
                if e in (2,6):
                    p=a.old.layer_family(b,e,side)
                    check('original_family_specialization',all(f[k]==p[k] for k in ('n0','nstep','m0','mstep','y0','ystep','left_word','right_word')))
                for t0 in (0,1,3):
                    n=f['n0']+t0*f['nstep'];m=f['m0']+t0*f['mstep']
                    lv=a.old.path(n,f['left_word']);rv=a.old.path(m,f['right_word'])
                    check('point_path_target',lv[-1]==rv[-1])
                    check('point_exact_layer',a.old.v3(n)==b+f['h_order'])
                    check('original_support_bound',max(lv+rv)<=a.support_bound(n))
                    choices=a.candidates(n)
                    z=[z for z in choices if z['e']==e and z['bilateral']==side and z['b']==b]
                    check('finite_search_recovers_family',len(z)==1 and z[0]['target']<=m)
                    mv=a.old.make_move(n,z[0]['target'],z[0]['left_word'],z[0]['right_word'],'test')
                    check('exact_firstjet_equation',a.old.jet_d(mv.chain)==a.old.add_vectors({n:a.old.ONE},{mv.target:(-1,-mv.clock)}))
                    check('unit_clock_and_height',mv.target<n and len(mv.left_word)+len(mv.right_word)<=max(24,(n-1).bit_length()-2+a.old.floor_log3(n)+6))
                family_rows.append({k:f[k] for k in ('b','e','bilateral','a_min','actual_layer','n0','nstep','m0','mstep')})
    # Exhaust finite original inputs against a larger direct template search.
    recovered=0
    for n in range(3,4000,2):
        got={(z['b'],z['e'],z['bilateral']) for z in a.candidates(n)}
        actual=set()
        if n%3==0:
            for b in range(1,a.old.v3(n)+1):
                for e in range(2,26,2):
                    for side in (False,True):
                        if n%(32 if side else 4)!=(27 if side else 3):continue
                        f=a.family(b,e,side)
                        if (n-f['n0'])%f['nstep']==0:actual.add((b,e,side))
        check('finite_search_vs_independent_larger_domain',got==actual)
        recovered+=bool(got)
    # Complete periodic comparison with predecessor for one genuinely new whole family.
    f=a.family(2,8,False);P=a.old.NEW_PERIOD;mask=a.old.catalogues()['new_mask']
    modulus=P
    oldf=[]
    for e in (2,6):
        for side in (False,True):
            g=a.old.layer_family(f['actual_layer'],e,side);oldf.append(g)
            modulus=math.lcm(modulus,g['nstep'])
    tperiod=modulus//math.gcd(modulus,f['nstep'])
    root_residues=[]
    for t0 in range(tperiod):
        n=f['n0']+f['nstep']*t0
        isroot=bool(mask[n%P]) and all((n-g['n0'])%g['nstep'] for g in oldf)
        check('new_family_old_root',isroot)
        check('old_rules_fail',a.old.choose_move(n,2) is None)
        root_residues.append([t0,n%P])
    # Retractions: exact equations and old/new nesting, without global coverage claims.
    oldr=a.old.Retraction(2);newr=a.Retraction()
    seeds=list(range(1,513,2))+[20241207,20241207+f['nstep'],600089787,4405583871]
    for n in seeds:
        v={n:a.old.ONE};d=a.old.jet_d(v)
        H=newr.H(v);Q=newr.Q(v);F=newr.F(v)
        check('vertex_homotopy',a.old.jet_d(H)==a.old.add_vectors(v,a.old.scale((-1,0),Q)))
        check('Q_idempotent',newr.Q(Q)==Q)
        check('F_idempotent',newr.F(F)==F)
        check('chain_equation',a.old.jet_d(F)==newr.Q(d))
        check('H_Q_zero',newr.H(Q)=={})
        check('F_H_zero',newr.F(H)=={})
        check('nested_edge_forward',newr.F(oldr.F(v))==F)
        check('nested_edge_reverse',oldr.F(F)==F)
        K=a.old.add_vectors(H,a.old.scale((-1,0),oldr.H(v)))
        check('new_correction_in_old_image',oldr.F(K)==K)
        check('constant_coefficient_bound',sum(abs(c[0]) for c in H.values())<=a.term_bound(n))
        check('linear_coefficient_bound',sum(abs(c[1]) for c in H.values())<=a.term_bound(n)**2)
    controls=[lambda:a.family(0,8,False),lambda:a.family(1,3,False),lambda:a.family(1,True,False),
              lambda:a.candidates(0),lambda:a.candidates(4),lambda:a.candidates(True),
              lambda:a.old.make_move(20241207,20241209,(1,),(), 'bad'),
              lambda:a.old.path(20241207,(2,)),lambda:a.old.add_vectors({3:(1,0.5)}),
              lambda:a.family(True,2,False),lambda:a.family(1,2,0),lambda:a.family(1,2.0,False),
              lambda:a.move(20241207,1),lambda:a.Retraction(0)]
    for fn in controls:check('invalid_control_rejected',negative(fn))
    examples=[]
    for n in (20241207,600089787,4405583871):
        z=a.candidates(n)[0];mv=a.old.make_move(n,z['target'],z['left_word'],z['right_word'],'example')
        examples.append({**z,'left_path':list(mv.left_values),'right_path':list(mv.right_values),
                         'chain':{str(n):list(c) for n,c in mv.chain.items()},
                         'new_root':newr.resolve(n)[0],'old_root':oldr.resolve(n)[0],
                         'bound':a.support_bound(n)})
    return {'status':'PASS','claims_global_collatz':False,'counts':COUNTS,'total_exact_checks':sum(COUNTS.values()),
            'family_test_domain':{'b':[1,16],'even_e':[2,32],'selectors':[False,True],'families':len(family_rows),'point_parameters':[0,1,3]},
            'family_rows_sha256':hashlib.sha256(json.dumps(family_rows,sort_keys=True).encode()).hexdigest(),
            'finite_input_domain':[1,3999],'sources_with_template':recovered,
            'whole_new_family':f,'old_root_parameter_period':tperiod,'old_root_residues':root_residues,
            'retraction_seed_count':len(seeds),'examples':examples,'negative_controls':len(controls)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--check',type=Path);q=p.parse_args()
    result=run();data=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    if q.check:a.need(data==q.check.read_bytes(),'recorded-result mismatch')
    if q.output:q.output.write_bytes(data)
    print(json.dumps({'status':'PASS','exact_checks':result['total_exact_checks'],'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}))
if __name__=='__main__':main()
