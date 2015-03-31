/* 
 * File:   genome.h
 * Author: shine
 *
 * Created on October 14, 2013, 7:34 AM
 */

#ifndef GENOME_H
#define	GENOME_H

#include<list>
#include<set>

using namespace std;

class Chromosome:public list<int>{
public:
    int chrID; // for compare
    bool circular; //linear
    set<int> genes; //obtain sets of G A B, cal # of shared genes
    
    //no duplication
};

class Genome:public list<Chromosome>{
public:
//    string genomeID; 
    set<int> genes; //obtain sets of G A B, cal # of shared genes
   // for stat: # of shared genes
};


#endif	/* GENOME_H */

