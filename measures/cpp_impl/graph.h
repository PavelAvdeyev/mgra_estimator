/* 
 * File:   graph.h
 * Author: shine
 *
 * Created on October 14, 2013, 8:02 AM
 */

#ifndef GRAPH_H
#define	GRAPH_H

#include<string>
#include "adjacency.h"

using namespace std;

class Component:public list<Adjacency>{
public:
    int id;//?
    string type; //"", "cycle", "AA", "AB", "BA", "BB".
    
};

class Graph:public list<Component>{
public:
    int stat();// # cycles + 1/2 # of "AB" path
};

class ReducedComponent:public list<string>{ //must be path, list of types of runs "A" "B" "A"; cycle start with A-run;
public:
    string type_path; //"", "cycle", "AA", "AB", "BB".            
    string type_run; // AA, BB paths: "", "A", "B", "AB"
                 // AB path: "", "A", "B". "AB", "BA"
                 // cycle: no type; 
};
class ReducedGraph:public list<ReducedComponent>{
public:
    int stat();// landa = [(#run + 1 )/2 ]; sum up of weighted pairs of ReducedComponents.
};
#endif	/* GRAPH_H */

