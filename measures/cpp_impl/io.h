/* 
 * File:   io.h
 * Author: shine
 *
 * Created on September 26, 2013, 1:13 PM
 */

#ifndef IO_H
#define	IO_H

#include <stdlib.h> 
#include <iostream>
#include <istream>
#include <fstream>
#include <sstream>
#include <set>
#include <list>
#include <string>
#include "genome.h"

using namespace std;

    
class IO{
public:
//    set<Adjacency,AdjComp> ImportAdjacencies(const char * address);
    Genome ImportGenome(const char * address);
};

Genome IO::ImportGenome(const char* address){
    string word, line;
    int id;
    ifstream input;
    
    Genome g;
    input.open(address);
    if(input.is_open()){        
//        cerr << "Open: " << address << endl;
        
        while (input.good()) {
            // abandon non chromosome lines;
            if((char)input.peek()=='\n' || (char)input.peek()=='>' || (char)input.peek()=='#' || input.peek()==-1){
                line ="";
                getline(input,line);
//                cerr << "Non chr line: " << line << endl;
                continue;
            }
            
            // readin the chromosome;
            Chromosome chr;
            getline(input,line);
//            cerr << "Chr: " << endl;
            stringstream read(line);
            while(read.good()){
                read >> word;
                if(word == "$" ){
                    chr.circular=false;
                }
                else if(word == "@" || word == ";"){
                    chr.circular=true;
                }
                else if(word == "#"){ // comments symbol
                    break;
                }
                else {
                    stringstream convert(word);
                    if (convert >> id) {
                        chr.push_back(id);
                        chr.genes.insert(abs(id) );
                    }                  
                    else {
                        cerr << "Error: ImportGenomes, cannot convert string to int, " << word << endl;
                    }
                }
            }
            
            g.push_back(chr);
            g.genes.insert(chr.genes.begin(),chr.genes.end());
            // print the chromosome;
//            if(chr.circular){
//                cerr << "Circular chr: ";
//            }
//            else{
//                cerr << "Linear chr: ";
//            }
//            for(Chromosome::iterator it=chr.begin();it!=chr.end();it++){
//                cerr << *it << " \t";
//            }
//            cerr <<endl;
        }
    }
    else {
        cerr << "Fail to open: " << address << endl;
    }
    return g;
}

//set<Adjacency,AdjComp> IO::ImportAdjacencies(const char * address){
//    set<Adjacency,AdjComp> AS;
//    ifstream input;
//    string word, prev_word, cur_word, next_word;
//    int id;
//    list<string> gene_list;
//    bool flag=false;
//    
//    input.open(address);
//    if(input.is_open()){
//        cerr << "open: " << address << endl;
//        while (input >> word) {
//            if(word == "("){
//                gene_list.push_back("oo");
//                flag = true;
//            }
//            else if(word == ")"){
//                gene_list.push_back("oo");
//                flag = false;
//                bool flag_start = false;
//                for(list<string>::iterator it=gene_list.begin();it!=gene_list.end();it++){
//                    string gene = *it;
//                    if(!flag_start && gene=="oo"){//start: 
//                        prev_word = "oo";
//                        cur_word = "";
//                        next_word = "";
//                        flag_start = true;
//                        continue;
//                    }
//                    else if(flag_start && gene=="oo") {//end: 
//                        cur_word = "oo";
//                        next_word = "";
//                        flag_start = false;
//                    }
//                    else if(flag_start && gene != "oo"){
//                        stringstream convert(gene);
//                        if (convert >> id) {
//                            if (id >= 0) {
//                                cur_word = gene;
//                                cur_word.append("T");
//                                next_word = gene;
//                                next_word.append("H");
//                            } else { // id < 0
//                                gene.erase(gene.begin());
//                                cur_word = gene;
//                                cur_word.append("H");
//                                next_word = gene;
//                                next_word.append("T");
//                            }
//                        }
//                        else
//                            cerr << "Unexpected name that is not gene between delimeter ( ). Location: " << address << ", " << gene << endl;
//                    }
//                    else // not within a chr; not infinite point ; should not be a gene id
//                        continue;
//                    
//                    //cout << prev_word << " --- " << cur_word << ";\t";
//                    AS.insert(Adjacency(prev_word,cur_word));
//                    prev_word = next_word;
//                }
//                cout << endl;
//                gene_list.clear();
//            }
//            else{
//                if(flag){
//                    gene_list.push_back(word);
//                }
//            }
//        }
//    }
//    else{
//        cerr << "cannot open file: " << address << endl;
//    }
//    input.close();
//    return AS;
//}
#endif	/* IO_H */

