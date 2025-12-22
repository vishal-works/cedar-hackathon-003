#!/usr/bin/env python3
"""
Comprehensive Knowledge Graph Analysis Script.

This script analyzes the Neo4j knowledge graph for:
- Duplicate entities
- Orphan nodes
- Edge type inconsistencies
- Data quality issues
- Coverage gaps
"""

import os
from collections import Counter
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
)

print('=' * 80)
print('                    KNOWLEDGE GRAPH ANALYSIS REPORT')
print('=' * 80)

with driver.session() as session:
    
    # =========================================================================
    # 1. DUPLICATE ENTITY ANALYSIS
    # =========================================================================
    print('\n' + '=' * 80)
    print('1. DUPLICATE ENTITY ANALYSIS')
    print('=' * 80)
    
    result = session.run('''
        MATCH (n:Entity)
        WITH n.name as name, collect(n) as nodes, count(*) as cnt
        WHERE cnt > 1
        RETURN name, cnt, [node in nodes | labels(node)] as labels
        ORDER BY cnt DESC
        LIMIT 20
    ''')
    
    duplicates = list(result)
    print(f'\nDuplicate Entity Names: {len(duplicates)} found')
    for r in duplicates[:10]:
        name = r["name"][:50] if r["name"] else "NULL"
        print(f'  "{name}..." appears {r["cnt"]} times')
    
    # =========================================================================
    # 2. ORPHAN NODE ANALYSIS
    # =========================================================================
    print('\n' + '=' * 80)
    print('2. ORPHAN NODE ANALYSIS (entities with no RELATES_TO)')
    print('=' * 80)
    
    result = session.run('''
        MATCH (n:Entity)
        WHERE NOT (n)-[:RELATES_TO]-() AND NOT (n)<-[:RELATES_TO]-()
        RETURN labels(n) as labels, count(*) as cnt
        ORDER BY cnt DESC
    ''')
    
    orphans = list(result)
    total_orphans = sum(r['cnt'] for r in orphans)
    print(f'\nTotal Orphan Entities: {total_orphans}')
    for r in orphans:
        print(f'  {str(r["labels"]):40} {r["cnt"]}')
    
    # =========================================================================
    # 3. EDGE TYPE INCONSISTENCY
    # =========================================================================
    print('\n' + '=' * 80)
    print('3. EDGE TYPE INCONSISTENCY (same meaning, different names)')
    print('=' * 80)
    
    result = session.run('''
        MATCH ()-[r:RELATES_TO]->()
        RETURN r.name as edge_type, count(*) as cnt
        ORDER BY edge_type
    ''')
    
    edge_types = [(r['edge_type'], r['cnt']) for r in result]
    
    similar_groups = {
        'CONTAINS': ['CONTAINS', 'Contains'],
        'APPLIES_IN': ['APPLIES_IN', 'AppliesIn', 'APPLIESIN'],
        'ALLOWS_USE': ['ALLOWS_USE', 'AllowsUse', 'ALLOWSUSE'],
        'GOVERNED_BY': ['GOVERNED_BY', 'GovernedBy'],
        'SOURCED_FROM': ['SOURCED_FROM', 'SourcedFrom'],
        'HAS_CONSTRAINT': ['HAS_CONSTRAINT', 'HasConstraint', 'HASCONSTRAINT'],
        'HAS_CONDITION': ['HAS_CONDITION', 'HasCondition'],
    }
    
    print('\nInconsistent Edge Types to Normalize:')
    for canonical, variants in similar_groups.items():
        counts = {v: 0 for v in variants}
        for et, cnt in edge_types:
            if et in variants:
                counts[et] = cnt
        non_zero = {k: v for k, v in counts.items() if v > 0}
        if len(non_zero) > 1:
            total = sum(non_zero.values())
            print(f'  {canonical}: {non_zero} → Total: {total}')
    
    # =========================================================================
    # 4. ENTITY LABEL ANALYSIS
    # =========================================================================
    print('\n' + '=' * 80)
    print('4. ENTITY LABEL ANALYSIS')
    print('=' * 80)
    
    result = session.run('''
        MATCH (n:Entity)
        WHERE NOT (n:Zone OR n:Rule OR n:UseType OR n:Constraint OR 
                   n:Jurisdiction OR n:Override OR n:Condition OR n:DocumentSource)
        RETURN count(n) as cnt
    ''')
    untyped = result.single()['cnt']
    
    result = session.run('MATCH (n:Entity) RETURN count(n) as cnt')
    total_entities = result.single()['cnt']
    
    print(f'\nTotal Entities: {total_entities}')
    print(f'Untyped Entities (only Entity label): {untyped}')
    print(f'Typed Entities: {total_entities - untyped}')
    print(f'Typing Coverage: {(total_entities - untyped) / total_entities * 100:.1f}%')
    
    # Sample untyped entities
    result = session.run('''
        MATCH (n:Entity)
        WHERE NOT (n:Zone OR n:Rule OR n:UseType OR n:Constraint OR 
                   n:Jurisdiction OR n:Override OR n:Condition OR n:DocumentSource)
        RETURN n.name as name, n.summary as summary
        LIMIT 15
    ''')
    untyped_samples = list(result)
    print('\nSample Untyped Entities:')
    for r in untyped_samples[:10]:
        name = r["name"][:60] if r["name"] else "NULL"
        print(f'  - {name}')
    
    # =========================================================================
    # 5. RELATIONSHIP PATTERN ANALYSIS
    # =========================================================================
    print('\n' + '=' * 80)
    print('5. RELATIONSHIP PATTERN ANALYSIS')
    print('=' * 80)
    
    result = session.run('''
        MATCH (a)-[r:RELATES_TO]->(b)
        WITH labels(a)[0] as from_type, r.name as edge, labels(b)[0] as to_type, count(*) as cnt
        WHERE cnt > 5
        RETURN from_type, edge, to_type, cnt
        ORDER BY cnt DESC
        LIMIT 25
    ''')
    
    print('\nTop Relationship Patterns (From → Edge → To):')
    for r in result:
        print(f'  {r["from_type"]:15} --[{r["edge"]:20}]--> {r["to_type"]:15} ({r["cnt"]})')
    
    # =========================================================================
    # 6. DATA QUALITY ISSUES
    # =========================================================================
    print('\n' + '=' * 80)
    print('6. DATA QUALITY ISSUES')
    print('=' * 80)
    
    # Empty names
    result = session.run('''
        MATCH (n:Entity)
        WHERE n.name IS NULL OR n.name = ''
        RETURN count(n) as cnt
    ''')
    empty_names = result.single()['cnt']
    print(f'\nEntities with empty/null names: {empty_names}')
    
    # Very short names
    result = session.run('''
        MATCH (n:Entity)
        WHERE size(n.name) < 3
        RETURN n.name as name, labels(n) as labels
        LIMIT 10
    ''')
    short_names = list(result)
    print(f'Entities with very short names (<3 chars): {len(short_names)}')
    for r in short_names[:5]:
        print(f'  "{r["name"]}" - {r["labels"]}')
    
    # Very long names
    result = session.run('''
        MATCH (n:Entity)
        WHERE size(n.name) > 100
        RETURN count(n) as cnt
    ''')
    long_names = result.single()['cnt']
    print(f'Entities with very long names (>100 chars): {long_names}')
    
    # Sample long names
    if long_names > 0:
        result = session.run('''
            MATCH (n:Entity)
            WHERE size(n.name) > 100
            RETURN n.name as name, labels(n) as labels
            LIMIT 5
        ''')
        print('  Samples:')
        for r in result:
            print(f'    "{r["name"][:80]}..."')
    
    # =========================================================================
    # 7. COVERAGE ANALYSIS
    # =========================================================================
    print('\n' + '=' * 80)
    print('7. COVERAGE ANALYSIS')
    print('=' * 80)
    
    # Zones with no rules
    result = session.run('''
        MATCH (z:Zone)
        WHERE NOT (z)<-[:RELATES_TO]-(:Rule) AND NOT (z)-[:RELATES_TO]->(:Rule)
        RETURN count(z) as cnt
    ''')
    zones_no_rules = result.single()['cnt']
    
    result = session.run('MATCH (z:Zone) RETURN count(z) as cnt')
    total_zones = result.single()['cnt']
    
    print(f'\nZones with no linked Rules: {zones_no_rules}/{total_zones} ({zones_no_rules/total_zones*100:.1f}%)')
    
    # Rules with no constraints
    result = session.run('''
        MATCH (r:Rule)
        WHERE NOT (r)-[:RELATES_TO]->(:Constraint)
        RETURN count(r) as cnt
    ''')
    rules_no_constraints = result.single()['cnt']
    
    result = session.run('MATCH (r:Rule) RETURN count(r) as cnt')
    total_rules = result.single()['cnt']
    
    print(f'Rules with no Constraints: {rules_no_constraints}/{total_rules} ({rules_no_constraints/total_rules*100:.1f}%)')
    
    # Constraints with no conditions
    result = session.run('''
        MATCH (c:Constraint)
        WHERE NOT (c)-[:RELATES_TO]->(:Condition)
        RETURN count(c) as cnt
    ''')
    constraints_no_conditions = result.single()['cnt']
    
    result = session.run('MATCH (c:Constraint) RETURN count(c) as cnt')
    total_constraints = result.single()['cnt']
    
    print(f'Constraints with no Conditions: {constraints_no_conditions}/{total_constraints} ({constraints_no_conditions/total_constraints*100:.1f}%)')
    
    # =========================================================================
    # 8. EDGE TYPE PROLIFERATION
    # =========================================================================
    print('\n' + '=' * 80)
    print('8. EDGE TYPE PROLIFERATION')
    print('=' * 80)
    
    result = session.run('''
        MATCH ()-[r:RELATES_TO]->()
        RETURN count(DISTINCT r.name) as unique_edge_types
    ''')
    unique_edges = result.single()['unique_edge_types']
    print(f'\nTotal Unique Edge Types: {unique_edges}')
    print('(Expected: ~8-10 from ontology, but LLM created many more)')
    
    # Edge types with only 1-2 occurrences (noise)
    result = session.run('''
        MATCH ()-[r:RELATES_TO]->()
        WITH r.name as edge_type, count(*) as cnt
        WHERE cnt <= 2
        RETURN count(*) as rare_types
    ''')
    rare_types = result.single()['rare_types']
    print(f'Rare Edge Types (≤2 occurrences): {rare_types}')
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print('\n' + '=' * 80)
    print('                         SUMMARY & RECOMMENDATIONS')
    print('=' * 80)
    
    issues = []
    if len(duplicates) > 0:
        issues.append(f'- {len(duplicates)} duplicate entity names need merging')
    if total_orphans > 0:
        issues.append(f'- {total_orphans} orphan entities need linking or removal')
    if untyped > 0:
        issues.append(f'- {untyped} untyped entities need classification')
    if unique_edges > 20:
        issues.append(f'- {unique_edges} edge types need normalization (expected ~10)')
    if long_names > 0:
        issues.append(f'- {long_names} entities have overly long names')
    
    print('\nIssues Found:')
    for issue in issues:
        print(f'  {issue}')
    
    print('\nRecommended Cleanup Actions:')
    print('  1. Normalize edge type names (UPPER_CASE standard)')
    print('  2. Merge duplicate entities')
    print('  3. Remove or link orphan nodes')
    print('  4. Classify untyped entities')
    print('  5. Clean up rare/noisy edge types')
    print('  6. Remove Entity label from typed nodes')

print('\n' + '=' * 80)
print('                         END OF ANALYSIS')
print('=' * 80)

driver.close()

