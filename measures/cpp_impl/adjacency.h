/* 
 * File:   adjacency.h
 * Author: shine
 *
 * Created on September 26, 2013, 11:41 AM
 */

#ifndef ADJACENCY_H
#define	ADJACENCY_H

#include <utility>
#include <string>
#include <sstream>
#include <fstream>
#include <set>
#include <vector>
#include "genome.h"

using namespace std;

class Adjacency:public pair<string,string> {
public:    
    vector<int> labels; // "","id" can be negative, representing the strand
    string side; // "", "A", "B" 
    
    // once created should not be modified
    Adjacency(){};
    Adjacency(string a, string b){
        this->first = a;
        this->second = b;
    };
    Adjacency(string a, string b, string s){
        this->first = a;
        this->second = b;
        this->side=s;
    };
    bool NotTelomere(){
        return this->first!="oo"&&this->second!="oo";
    };
    bool Contain(string s){
        return this->first==s||this->second==s;
    };
    void Print(ofstream &out) const{
        out << this->side << ":(" << this->first << ", ";
        for(vector<int>::const_iterator it=this->labels.begin();it!=this->labels.end();it++){
            out << *it << ", ";
        }
        out << this->second << ")";
    };
    void PrintOnScreen() const{
        cerr << this->side << ":(" << this->first << ", ";
        for(vector<int>::const_iterator it=this->labels.begin();it!=this->labels.end();it++){
            cerr << *it << ", ";
        }
        cerr << this->second << ")";
    };
};

bool operator== (const Adjacency& lhs, const Adjacency& rhs){ // not consider the labels
    if (lhs.side !=rhs.side )
        return false;
    return ( lhs.first==rhs.first && lhs.second==rhs.second )
        || ( lhs.first==rhs.second && lhs.second==rhs.first ); 
};

bool operator!=(const Adjacency& lhs, const Adjacency& rhs){
    return !(lhs==rhs);
}

bool operator < (const Adjacency& lhs, const Adjacency& rhs){  
        if(lhs.side!=rhs.side)
            return lhs.side < rhs.side;                
        
        string lS = lhs.first>lhs.second?lhs.second:lhs.first;
        string lG = lhs.first>lhs.second?lhs.first:lhs.second;
        string rS = rhs.first>rhs.second?rhs.second:rhs.first;
        string rG = rhs.first>rhs.second?rhs.first:rhs.second;
        
        if(lS==rS)
            return lG < rG;
        else
            return lS < rS;
};

bool IsSame(Adjacency lhs, Adjacency rhs) { 
    // Direction of the labels between the extremities should be considered.
    if ( lhs.first==rhs.first && lhs.second==rhs.second ) {
        return lhs.labels == rhs.labels;
    }
    else if ( lhs.first==rhs.second && lhs.second==rhs.first ) {
        vector <int> rhs_labels_reverse = rhs.labels;
        reverse(rhs_labels_reverse.begin(), rhs_labels_reverse.end());
        
        return lhs.labels == rhs_labels_reverse;        
    }
    else 
        return false;
}

struct AdjComp {
    bool operator() (Adjacency lhs, Adjacency rhs) {
        if(lhs.side!=rhs.side)
            return lhs.side < rhs.side;                
                
        string lS = lhs.first>lhs.second?lhs.second:lhs.first;
        string lG = lhs.first>lhs.second?lhs.first:lhs.second;
        string rS = rhs.first>rhs.second?rhs.second:rhs.first;
        string rG = rhs.first>rhs.second?rhs.first:rhs.second;
                
        if(lS==rS)
            return lG < rG;
        else
            return lS < rS;
    }
};

//bool Connected(Adjacency a, Adjacency b){
//    return 
//};


class GenomeAG:public set<Adjacency, AdjComp>{
public:
    string side; // Genome "A", "B"
    GenomeAG(){};
    GenomeAG(Genome g, set<int> marks, string s){
        this->side=s;
        stringstream convert;
        for(Genome::iterator it1=g.begin();it1!=g.end();it1++){ // gene (end_right,end_left).
            string end_left="oo", end_right, suffix_left, suffix_right;
            Adjacency adj;
            vector<int> labels;
            
            for(Chromosome::iterator it2=it1->begin(); it2!=it1->end(); it2++ ){ // start with right end
                int gene = *it2, gene_id=abs(gene);
                if(gene>=0){ // (right, left) --- (right, left)
                    suffix_left="H";
                    suffix_right="T";
                }
                else{
                    suffix_left="T";
                    suffix_right="H";                    
                } 
                
                if(marks.count(gene_id)){  
                    labels.push_back(gene);
                }
                else{
                    convert << gene_id << suffix_right;
                    end_right = convert.str();
                    convert.str(std::string());
                    
                    adj=Adjacency(end_left,end_right,s);
                    adj.labels=labels;
                    this->insert(adj);
                    labels.clear();
                    
                    convert << gene_id << suffix_left;
                    end_left = convert.str();
                    convert.str(std::string());
                }
//                cerr << "(" << adj.first << ", ";
//                for(vector<int>::iterator it=adj.labels.begin();it!=adj.labels.end();it++){
//                    cerr << *it << ", ";
//                }
//                cerr << adj.second << ")\t";
            }
            end_right="oo";
            adj=Adjacency(end_left,end_right,s);
            adj.labels=labels;
            this->insert(adj);
            labels.clear();
        }
    };
};

#endif	/* ADJACENCY_H */

