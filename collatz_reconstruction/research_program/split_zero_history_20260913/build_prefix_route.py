"""Record bounded queries for the current prefix and spectral-predicate calculation."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CORPUS = Path('C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/Zeta-Function-Foundation')
queries = []
for terms in ['Tao Syracuse geometric', 'support idempotent Collatz', 'finite moments interpolation']:
    raw = subprocess.run([sys.executable, str(CORPUS / 'scripts/query_corpus.py'), '--layer', 'all',
                          '--index-level', 'canonical', '--limit-per-layer', '3', '--json', terms],
                         check=True, capture_output=True, text=True, encoding='utf-8')
    result = json.loads(raw.stdout)
    ids = [hit['unit_id'] for layer in result['layers'].values()
           for hit in layer['canonical']['results']]
    queries.append({'query': terms, 'layer': 'all', 'index_level': 'canonical',
                    'executed_utc': datetime.now(timezone.utc).isoformat(),
                    'reason': 'Bounded source route for fixed-sum Syracuse paths, support histories, and moment interpolation; returned items remain unread unless specified below.',
                    'result_unit_ids': ids})
now = datetime.now(timezone.utc).isoformat()
sources = []

def source(kind, ident, path, loci, sections, edge):
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    sources.append({'source_class': kind, 'publication_unit_or_source_id': ident,
                    'exact_locators': [path + ':' + locus for locus in loci],
                    'relevance_edge': edge,
                    'toc_or_section_check': {'status': 'checked', 'checked_utc': now,
                                             'relevant_sections': sections},
                    'reading_status': 'fully_content_read_for_current_dependency',
                    'content_loci_read': loci, 'dependencies': [], 'notes': 'SHA256 ' + digest})

source('research_literature', 'PUBUNIT-847E4E7212BFCD7A613CA573',
       'C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1909.03562v7/collatz.tex',
       ['225-278'], ['Syracuse formulation; geometric random variable; distribution of n-Syracuse valuation'],
       'Exact product geometric law and affine valuation convention. The conditioned finite-packet law is proved directly; no stronger orbit theorem is attributed to Tao.')
source('local_unpublished_work', 'PUBUNIT-004F3DB5D12B4A71C77EDE18',
       'C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/automata/v4/collatz_dyadic_dilation_note.tex',
       ['526-559', '1149-1181'], ['Packet cardinalities', 'Exact Gibbs law'],
       'Local notes already contain the composition count and geometric one-letter Gibbs law. Conditioning on length and exponent sum is checked without importing broader BCM interpretations.')
source('local_unpublished_work', 'SZ-HURWITZ-H1-H13',
       'C:/Users/LOCAL_USER/Documents/math/output/split_zero_rh_tandem_2026-09-12/tex/historical_hurwitz_jets.tex',
       ['23-61', '231-301'], ['Compact Hurwitz inputs', 'Complete zero cluster'],
       'Equality of actual full-cluster jets is equivalent to equality of input moments at any nontrivial zero, with multiplicity retained. Current continuation source postdates the frozen index.')
source('local_unpublished_work', 'COL-ODD-CYLINDER-COMPANION',
       str(ROOT.parents[1] / 'research_companion/chapters/02_two_adic_survivor_coding_and_exact_interface_boundaries.tex').replace('\\', '/'),
       ['24-182'], ['Partial odd map', 'Exact residue cylinders'],
       'Exact odd 2-adic cylinders, prefix inclusions, exceptional countable set. Supplies arithmetic residue coordinates and Haar cylinder weights.')
sources.append({'source_class': 'research_literature', 'publication_unit_or_source_id': 'DLMF-3-3-I',
                'exact_locators': ['https://dlmf.nist.gov/3.3.E1', 'https://dlmf.nist.gov/3.3.E2', 'https://dlmf.nist.gov/3.3.E3_1'],
                'relevance_edge': 'Classical Lagrange and barycentric formulas used to prove exact observable-dependent jet order.',
                'toc_or_section_check': {'status': 'checked', 'checked_utc': now, 'relevant_sections': ['3.3(i) Lagrange interpolation']},
                'reading_status': 'fully_content_read_for_current_dependency',
                'content_loci_read': ['3.3.1-3.3.3_2'], 'dependencies': []})
route = {'schema_version': 1, 'topic_id': 'COL-SZ-PREFIX-SPECTRAL-20260913',
         'topic': 'Exact fixed-sum Collatz prefix fibres, conditioned geometric laws, and observable-dependent spectral jet order',
         'workspace': str(ROOT), 'corpus_entrypoint': str(CORPUS / 'config/literature_index_entrypoint.json'),
         'updated_utc': now, 'mathematical_objects': ['positive compositions', 'odd 2-adic cylinders', 'finite pushforward kernels', 'full Hurwitz zero-cluster jets', 'moment functionals'],
         'queries': queries, 'sources': sources, 'unresolved_dependencies': [],
         'refresh_reason': 'Continue the user-requested Split Zero application: replace a generic prefix-map example by exact fixed-sum fibres and prove the minimal jet order for individual arithmetic observables.',
         'anti_loop_note': 'No index rebuild or whole-library sweep. No priority claim. Generic query hits are not admitted as source theorems.'}
(ROOT / 'prefix_topic_route.json').write_text(json.dumps(route, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps({'status': 'PASS', 'queries': len(queries), 'sources': len(sources)}))
