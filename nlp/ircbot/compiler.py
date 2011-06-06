"""
question = sentence, QMARK;

assertion = sentence, DOT;

sentence = fact;

sentence = copula;

copula = varsymbol, ISA, SYMBOL;

fact = varsymbol, predicate, time;

varsymbol = SYMBOL;

varsymbol = VAR;

time = time, time;

time = TIME;

time = NOW;

time = VAR;

predicate = VAR;

predicate = varsymbol, items;

items = modifier, items;

items = ;

modifier = SYMBOL, modificator;

modificator = SYMBOL;

modificator = predicate;

modificator = NUMBER;

modificator = VAR;
"""
import re
import nl
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from nlp.ircbot.lexer import tokens

VAR_PAT = re.compile(r'([A-Z][a-zA-Z]+)(\d+)')


# UTILS

def _from_var(p):
    match = VAR_PAT.match(p[1])
    cls = nl.utils.get_class(match.group(1))
    return cls(p[1])

# BNF

def p_question(p):
    'question : sentence QMARK'
    response = nl.kb.ask(p[1])
    p[0] = str(response)

def p_assertion(p):
    'assertion : sentence DOT'
    response = nl.kb.tell(p[1])
    p[0] = str(response)

def p_sentence_fact(p):
    'sentence : fact'
    p[0] = p[1]

def p_sentence_copula(p):
    'sentence : copula'
    p[0] = p[1]

def p_copula(p):
    'copula : varsymbol ISA SYMBOL'
    cls = nl.utils.get_class(p[3].capitalize())
    p[0] = cls(p[1])

def p_fact(p):
    'fact : varsymbol predicate time'
    p[0] = nl.Fact(*p[1:])

def p_varsymbol_symbol(p):
    'varsymbol : SYMBOL'
    p[0] = nl.utils.get_symbol(p[1]) or p[1] # get_symbol intenta recuperar una clase y si no puede pregunta por una thing

def p_varsymbol_var(p):
    'varsymbol : VAR'
    p[0] = _from_var(p)

def p_time_time_time(p):
    'time : time time'
    p[0] = nl.Duration(start=p[1], end=p[2])

def p_time_time(p):
    'time : TIME'
    p[0] = nl.Instant(p[1])

def p_time_now(p):
    'time : NOW'
    p[0] = nl.Instant('now')

def p_time_var(p):
    'time : VAR'
    p[0] = _from_var(p)

def p_predicate_var(p):
    'predicate : VAR'
    p[0] = _from_var(p)

def p_predicate(p):
    'predicate : varsymbol items'
    p[0] = p[1](**dict(p[2]))
 
def p_items(p):
    'items : modifier items'
    p[0] = [p[1]] + p[2]
 
def p_items_empty(p):
    'items : empty'
    p[0] = []
 
def p_empty(p):
    'empty :'
    pass

def p_modifier(p):
    'modifier : SYMBOL modificator'
    p[0] = (p[1], p[2])

def p_modificator_symbol(p):
    'modificator : SYMBOL'
    p[0] = nl.utils.get_symbol(p[1]) # get_symbol intenta recuperar una clase y si no puede pregunta por una thing

def p_modificator_predicate(p):
    'modificator : predicate'
    p[0] = p[1]

def p_modificator_number(p):
    'modificator : NUMBER'
    p[0] = p[1]

def p_modificator_var(p):
    'modificator : VAR'
    p[0] = _from_var(p)


# Error rule for syntax errors
def p_error(p):
    print "Syntax error!! ",p

# Build the parser
# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")
yacc.yacc()
