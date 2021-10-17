
from __future__ import with_statement
import contextlib
import sys
import time

from pyke import knowledge_engine, krb_traceback, goal

# Compile and load .krb files in same directory that I'm in (recursively).
engine = knowledge_engine.engine(__file__)

fc_goal = goal.compile('kfacts.how_related($object1, $object2, $relationship)')

def fc_all_rules():
    engine.reset()
    engine.activate('fc_krule')
    with fc_goal.prove(engine) as gen:
        for vars, plan in gen:
            print "%s, %s : %s" % \
                    (vars['object1'], vars['object2'], vars['relationship'])
    print
    print "done"
    engine.print_stats()

def fc_person_environment(person1):
    engine.reset()
    engine.activate('fc_krule')
    print
    print
    print "Inference for %s - environment market" % person1
    weather = ""
    environment = ""
    with fc_goal.prove(engine, object1=person1) as gen:
        for vars, plan in gen:
            if vars['relationship'] == 'likes':
                weather = vars['object2']
            if vars['relationship'] == 'work_environment':
                environment = vars['object2']
    print "[%s likes %s weather and works %s]" % (person1, weather, environment )

def fc_neighbors(person1):
    engine.reset()
    engine.activate('fc_krule')

    print "Neighbors"
    with fc_goal.prove(engine, object1 = person1) as gen:
        for vars, plan in gen:
            if vars['relationship'] == 'neighbors':
                print "[%s %s are %s]" % (vars['object1'], vars['relationship'], vars['object2'] )

fc_all_rules()
fc_person_environment('ken')
fc_neighbors('ken')
