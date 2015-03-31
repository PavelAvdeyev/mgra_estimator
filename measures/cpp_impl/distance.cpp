/* 
 * File:   stat_branch.cpp
 * Author: shine
 *
 * Created on April 5, 2014, 1:22 PM
 */

#include <cstdlib>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <math.h>
#include <map>
#include <stack>

#include "genome.h"
#include "adjacency.h"
#include "io.h"
#include "graph.h"

using namespace std;

std::pair<int, int> Distance(Genome g1, Genome g2) {
    ofstream dist_log("/dev/null");
    // shared genes and marks, let the simulated genome be genome A and reconstructed genome be genome B
    Genome a = g1, b = g2;
    set<int> shared_genes, marks_a, marks_b;
    set_intersection(g1.genes.begin(), g1.genes.end(), g2.genes.begin(), g2.genes.end(), insert_iterator <set<int> >(shared_genes, shared_genes.begin()));
    set_difference(g1.genes.begin(), g1.genes.end(), g2.genes.begin(), g2.genes.end(), insert_iterator <set<int> >(marks_a, marks_a.begin()));
    set_difference(g2.genes.begin(), g2.genes.end(), g1.genes.begin(), g1.genes.end(), insert_iterator <set<int> >(marks_b, marks_b.begin()));
    int num_shared_genes = shared_genes.size();

    //    dist_log << "G1 size: " << g1.genes.size() << ", G2 size: " << g2.genes.size() << endl;
    //    dist_log << marks_a.size() << " marks in G1: " << endl;
    //    for(set<int>::iterator it=marks_a.begin(); it!=marks_a.end(); it++) {
    //        dist_log << *it << "\t";
    //    }
    //    dist_log << endl << marks_b.size() << " marks in G2: " << endl;
    //    for(set<int>::iterator it=marks_b.begin(); it!=marks_b.end(); it++) {
    //        dist_log << *it << "\t";
    //    }
    //    dist_log << endl;   

    // adjacency graph: adjacency -> connected components -> cycle/path -> shrinked cycle/path according to marks -> type
    GenomeAG a_ag(a, marks_a, "A");
    GenomeAG b_ag(b, marks_b, "B");

    //    dist_log << "G1 adj graph: " << endl;
    //    for(GenomeAG::iterator it1=a_ag.begin();it1!=a_ag.end();it1++){
    //        (*it1).Print(dist_log);  dist_log << "\t";
    //    }
    //    dist_log << endl << "G2 adj graph: " << endl;
    //    for(GenomeAG::iterator it1=b_ag.begin();it1!=b_ag.end();it1++){
    //        (*it1).Print(dist_log);  dist_log << "\t";
    //    }
    //    dist_log << endl;    

    //construct partial equivalence relation using multimap    
    multimap<Adjacency, Adjacency, AdjComp> connections;
    for (GenomeAG::iterator itA = a_ag.begin(); itA != a_ag.end(); itA++) {
        for (GenomeAG::iterator itB = b_ag.begin(); itB != b_ag.end(); itB++) {
            if ((itA->first == itB->first && itA->first != "oo") ||
                    (itA->first == itB->second && itA->first != "oo") ||
                    (itA->second == itB->first && itA->second != "oo") ||
                    (itA->second == itB->second && itA->second != "oo")) {
                connections.insert(pair<Adjacency, Adjacency>(*itA, *itB));
                connections.insert(pair<Adjacency, Adjacency>(*itB, *itA));
            }
        }
    }

    //    dist_log << "Adjacency equivalence relation btw G1 and G2 adj graph: " << endl;
    //    for(multimap<Adjacency,Adjacency,AdjComp>::iterator it=connections.begin();it!=connections.end();it++){
    //        it->first.Print(dist_log);
    //        dist_log << "\t -> ";
    //        it->second.Print(dist_log);
    //        dist_log << endl;
    //    }

    // Construct the ag graph
    //    dist_log << "Components: " << endl;
    Graph ag_graph;
    while (connections.size() > 0) {
        Component c; // list of the adjacencies;
        set<Adjacency, AdjComp> elements; // set of adjacencies in the component C -> exclude duplicated adjacency and later removal

        // 1st adjacency
        Adjacency a = (*connections.begin()).first;
        c.push_back(a);
        elements.insert(a);

        pair <multimap<Adjacency, Adjacency, AdjComp>::iterator, multimap<Adjacency, Adjacency, AdjComp>::iterator> ret; // iterator range to all mapped elements
        string left, right, new_left, new_right, flag; // record the 

        // begin the iteration 
        left = c.front().first;
        right = c.back().second;

        // iterate on left direction
        while (left != "oo" && flag != "cycle") {
            ret = connections.equal_range(c.front());
            int match_num = 0;
            new_left = left;
            for (multimap<Adjacency, Adjacency, AdjComp>::iterator it = ret.first; it != ret.second; it++) {
                if ((*it).second.Contain(left)) {
                    match_num++;
                    if (elements.find((*it).second) != elements.end()) {
                        flag = "cycle";
                    } else {
                        c.push_front((*it).second);
                        elements.insert((*it).second);
                        new_left = (*it).second.first == left ? (*it).second.second : (*it).second.first;
                    }
                }
            }
            left = new_left;

            if (match_num != 1) {
                dist_log << "Error: non/concurrent matched adj " << endl;
            }
        }

        // iterate on right direction
        while (right != "oo" && flag != "cycle") {
            ret = connections.equal_range(c.back());
            int match_num = 0;
            new_right = right;
            for (multimap<Adjacency, Adjacency, AdjComp>::iterator it = ret.first; it != ret.second; it++) {
                if ((*it).second.Contain(right)) {
                    match_num++;
                    if (elements.find((*it).second) != elements.end()) {
                        flag = "cycle";
                    } else {
                        c.push_back((*it).second);
                        elements.insert((*it).second);
                        new_right = (*it).second.first == right ? (*it).second.second : (*it).second.first;
                    }
                }
            }
            right = new_right;

            if (match_num != 1) {
                dist_log << "Error: non/concurrent matched adj " << endl;
            }
        }

        if (flag == "cycle")
            c.type = "cycle";
        else
            c.type = c.front().side + c.back().side;

        //        dist_log << c.type << ", ";
        //        for(Component::iterator it=c.begin();it!=c.end();it++){
        //            (*it).Print(dist_log);
        //            dist_log << ",\t";
        //        }
        //        dist_log << endl;

        ag_graph.push_back(c);
        // remove Component elements in the connections.
        for (set<Adjacency, AdjComp>::iterator it = elements.begin(); it != elements.end(); it++) {
            connections.erase(*it);
        }
    }

    // compress the ag graph and statistic on num of cycles and different paths
    int num_cycle = 0, num_AB = 0, num_BA = 0, num_AA = 0, num_BB = 0, num_empty = 0;
    ReducedGraph run_graph;

    for (Graph::iterator it1 = ag_graph.begin(); it1 != ag_graph.end(); it1++) {
        Component c = *it1;

        if (c.type == "cycle") { // put adj with mark A on the front of the cycle
            num_cycle++;

            Adjacency a0 = c.front(), a_split = c.front();
            for (Component::iterator it2 = c.begin(); it2 != c.end(); it2++) {
                if (it2->labels.size() > 0 && it2->side == "A") {
                    a_split = *it2;
                    break;
                }
            }

            while (a0 != a_split) {
                c.pop_front();
                c.push_back(a0);
                a0 = c.front();
            }
        } else if (c.type == "AB") {
            num_AB++;
        } else if (c.type == "BA") { // Turn "BA" -> "AB"
            num_BA++;
            c.reverse();
            c.type = "AB";
        } else if (c.type == "AA") {
            num_AA++;
        } else if (c.type == "BB") {
            num_BB++;
        } else if (c.type == "") {
            num_empty++;
        } else {
            dist_log << "impossible component" << endl;
        }

        // compress the component
        ReducedComponent runs;
        runs.type_path = c.type;
        string prev_side = "nothing";
        for (Component::iterator it2 = c.begin(); it2 != c.end(); it2++) {
            if (it2->labels.size() > 0 && it2->side != prev_side) {
                runs.push_back(it2->side);
                prev_side = it2->side;
            }
        }
        if (runs.size() > 0) {
            run_graph.push_back(runs);
        }
    }

    //    dist_log << "cycle num: " << num_cycle << "\tAB: " << num_AB << "\tBA: " << num_BA << "\tAA: " << num_AA << "\tBB: " << num_BB << "\tempty: " << num_empty << endl;

    // statistic on num_runs, landa = [num_rum+1/2]
    int sum_lambda = 0, num_AA_a = 0, num_AA_b = 0, num_AA_ab = 0,
            num_AB_a = 0, num_AB_b = 0, num_AB_ab = 0, num_AB_ba = 0,
            num_BB_a = 0, num_BB_b = 0, num_BB_ab = 0;
    for (ReducedGraph::iterator it = run_graph.begin(); it != run_graph.end(); it++) {
        int num_runs = 0, lambda = 0;
        num_runs = it->size();
        lambda = (int) ceil((num_runs + 1) / 2);
        sum_lambda += lambda;
        if (num_runs = 0) {
            cerr << "impossible 0 number of runs" << endl;
        } else if (num_runs % 2 == 1) { // odd runs
            it->type_run = (*it).front();
        } else if (num_runs % 2 == 0) { // even runs
            it->type_run = it->front() + it->back();
        } else {
            cerr << "impossible negative number of runs" << endl;
        }

        if (it->type_path == "AA") {
            if (it->type_run == "A")
                num_AA_a++;
            else if (it->type_run == "B")
                num_AA_b++;
            else if (it->type_run == "AB")
                num_AA_ab++;
        } else if (it->type_path == "BB") {
            if (it->type_run == "A")
                num_BB_a++;
            else if (it->type_run == "B")
                num_BB_b++;
            else if (it->type_run == "AB")
                num_BB_ab++;
        } else if (it->type_path == "AB") {
            if (it->type_run == "A")
                num_AB_a++;
            else if (it->type_run == "B")
                num_AB_b++;
            else if (it->type_run == "AB")
                num_AB_ab++;
            else if (it->type_run == "BA")
                num_AB_ba++;
        } else if (it->type_path == "cycle") {
            continue;
        } else {
            cerr << "impossible type of path: " << it->type_path << endl;
        }
    }
    //    dist_log << "sum_lambda: " << sum_lambda << "\tAA_a: " << num_AA_a << "\tAA_b: " << num_AA_b << "\tAA_ab: " << num_AA_ab 
    //            << "\tAB_a: " << num_AB_a << "\tAB_b: " << num_AB_b << "\tAB_ab: " << num_AB_ab << "\tAB_ba: " << num_AB_ba
    //            << "\tBB_a: " << num_BB_a << "\tBB_b: " << num_BB_b << "\tBB_ab: " << num_BB_ab << endl;

    // Calculate # of P Q T S
    int P = 0, Q = 0, T = 0, S = 0, M = 0, N = 0;
    // P
    if (num_AA_ab > 0 || num_BB_ab > 0) {
        int min = num_AA_ab > num_BB_ab ? num_BB_ab : num_AA_ab;
        if (min >= 0) {
            P += min;
            num_AA_ab -= min;
            num_BB_ab -= min;
        }
    }
    // Q 2AA_ab + BB_a + BB_b
    if (num_AA_ab > 0 || num_BB_a > 0 || num_BB_b > 0) {
        int min = (num_AA_ab / 2) > num_BB_a ? num_BB_a : (num_AA_ab / 2);
        min = min > num_BB_b ? num_BB_b : min;
        if (min >= 0) {
            Q += min;
            num_AA_ab -= 2 * min;
            num_BB_a -= min;
            num_BB_b -= min;
        }
    }
    // Q 2BB_ab + AA_a + AA_b
    if (num_BB_ab > 0 || num_AA_a > 0 || num_AA_b > 0) {
        int min = (num_BB_ab / 2) > num_AA_a ? num_AA_a : (num_BB_ab / 2);
        min = min > num_AA_b ? num_AA_b : min;
        if (min >= 0) {
            Q += min;
            num_BB_ab -= 2 * min;
            num_AA_a -= min;
            num_AA_b -= min;
        }
    }
    // T AA_ab + BB_a + AB_ab
    if (num_AA_ab > 0 || num_BB_a > 0 || num_AB_ab > 0) {
        int min = num_AA_ab > num_BB_a ? num_BB_a : num_AA_ab;
        min = min > num_AB_ab ? num_AB_ab : min;
        if (min >= 0) {
            T += min;
            num_AA_ab -= min;
            num_BB_a -= min;
            num_AB_ab -= min;
        }
    }
    // T AA_ab + BB_b + AB_ba
    if (num_AA_ab > 0 || num_BB_b > 0 || num_AB_ba > 0) {
        int min = num_AA_ab > num_BB_b ? num_BB_b : num_AA_ab;
        min = min > num_AB_ba ? num_AB_ba : min;
        if (min >= 0) {
            T += min;
            num_AA_ab -= min;
            num_BB_b -= min;
            num_AB_ba -= min;
        }
    }
    // T BB_ab + AA_a + AB_ba
    if (num_BB_ab > 0 || num_AA_a > 0 || num_AB_ba > 0) {
        int min = num_BB_ab > num_AA_a ? num_AA_a : num_BB_ab;
        min = min > num_AB_ba ? num_AB_ba : min;
        if (min >= 0) {
            T += min;
            num_BB_ab -= min;
            num_AA_a -= min;
            num_AB_ba -= min;
        }
    }
    // T BB_ab + AA_b + AB_ab
    if (num_BB_ab > 0 || num_AA_b > 0 || num_AB_ab > 0) {
        int min = num_BB_ab > num_AA_b ? num_AA_b : num_BB_ab;
        min = min > num_AB_ab ? num_AB_ab : min;
        if (min >= 0) {
            T += min;
            num_BB_ab -= min;
            num_AA_b -= min;
            num_AB_ab -= min;
        }
    }
    // T 2AA_ab + BB_a
    if (num_AA_ab > 0 || num_BB_a > 0) {
        int min = (num_AA_ab / 2) > num_BB_a ? num_BB_a : (num_AA_ab / 2);
        if (min >= 0) {
            T += min;
            num_AA_ab -= 2 * min;
            num_BB_a -= min;
        }
    }
    // T 2AA_ab + BB_b
    if (num_AA_ab > 0 || num_BB_b > 0) {
        int min = (num_AA_ab / 2) > num_BB_b ? num_BB_b : (num_AA_ab / 2);
        if (min >= 0) {
            T += min;
            num_AA_ab -= 2 * min;
            num_BB_b -= min;
        }
    }
    // T 2BB_ab + AA_a
    if (num_BB_ab > 0 || num_AA_a > 0) {
        int min = (num_BB_ab / 2) > num_AA_a ? num_AA_a : (num_BB_ab / 2);
        if (min >= 0) {
            T += min;
            num_BB_ab -= 2 * min;
            num_AA_a -= min;
        }
    }
    // T 2BB_ab + AA_b
    if (num_BB_ab > 0 || num_AA_b > 0) {
        int min = (num_BB_ab / 2) > num_AA_b ? num_AA_b : (num_BB_ab / 2);
        if (min >= 0) {
            T += min;
            num_BB_ab -= 2 * min;
            num_AA_b -= min;
        }
    }
    // S AA_a + BB_a
    if (num_AA_a > 0 || num_BB_a > 0) {
        int min = num_AA_a > num_BB_a ? num_BB_a : num_AA_a;
        if (min >= 0) {
            S += min;
            num_AA_a -= min;
            num_BB_a -= min;
        }
    }
    // S AA_b + BB_b
    if (num_AA_b > 0 || num_BB_b > 0) {
        int min = num_AA_b > num_BB_b ? num_BB_b : num_AA_b;
        if (min >= 0) {
            S += min;
            num_AA_b -= min;
            num_BB_b -= min;
        }
    }
    // S AB_ab + AB_ba
    if (num_AB_ab > 0 || num_AB_ba > 0) {
        int min = num_AB_ab > num_AB_ba ? num_AB_ba : num_AB_ab;
        if (min >= 0) {
            S += min;
            num_AB_ab -= min;
            num_AB_ba -= min;
        }
    }
    // S AA_ab + BB_a
    if (num_AA_ab > 0 || num_BB_a > 0) {
        int min = num_AA_ab > num_BB_a ? num_BB_a : num_AA_ab;
        if (min >= 0) {
            S += min;
            num_AA_ab -= min;
            num_BB_a -= min;
        }
    }
    // S AA_ab + BB_b
    if (num_AA_ab > 0 || num_BB_b > 0) {
        int min = num_AA_ab > num_BB_b ? num_BB_b : num_AA_ab;
        if (min >= 0) {
            S += min;
            num_AA_ab -= min;
            num_BB_b -= min;
        }
    }
    // S BB_ab + AA_a
    if (num_BB_ab > 0 || num_AA_a > 0) {
        int min = num_BB_ab > num_AA_a ? num_AA_a : num_BB_ab;
        if (min >= 0) {
            S += min;
            num_BB_ab -= min;
            num_AA_a -= min;
        }
    }
    // S BB_ab + AA_b
    if (num_BB_ab > 0 || num_AA_b > 0) {
        int min = num_BB_ab > num_AA_b ? num_AA_b : num_BB_ab;
        if (min >= 0) {
            S += min;
            num_BB_ab -= min;
            num_AA_b -= min;
        }
    }
    // S AA_ab + AB_ab
    if (num_AA_ab > 0 || num_AB_ab > 0) {
        int min = num_AA_ab > num_AB_ab ? num_AB_ab : num_AA_ab;
        if (min >= 0) {
            S += min;
            num_AA_ab -= min;
            num_AB_ab -= min;
        }
    }
    // S AA_ab + AB_ba
    if (num_AA_ab > 0 || num_AB_ba > 0) {
        int min = num_AA_ab > num_AB_ba ? num_AB_ba : num_AA_ab;
        if (min >= 0) {
            S += min;
            num_AA_ab -= min;
            num_AB_ba -= min;
        }
    }
    // S BB_ab + AB_ab
    if (num_BB_ab > 0 || num_AB_ab > 0) {
        int min = num_BB_ab > num_AB_ab ? num_AB_ab : num_BB_ab;
        if (min >= 0) {
            S += min;
            num_BB_ab -= min;
            num_AB_ab -= min;
        }
    }
    // S BB_ab + AB_ba
    if (num_BB_ab > 0 || num_AB_ba > 0) {
        int min = num_BB_ab > num_AB_ba ? num_AB_ba : num_BB_ab;
        if (min >= 0) {
            S += min;
            num_BB_ab -= min;
            num_AB_ba -= min;
        }
    }
    // S AA_ab + AA_ab
    if (num_AA_ab > 0) {
        int min = (num_AA_ab / 2);
        if (min >= 0) {
            S += min;
            num_AA_ab -= 2 * min;
        }
    }
    // S BB_ab + BB_ab
    if (num_BB_ab > 0) {
        int min = (num_BB_ab / 2);
        if (min >= 0) {
            S += min;
            num_BB_ab -= 2 * min;
        }
    }
    // M 2AB_ab + AA_b + BB_a    
    if (num_AB_ab > 0 || num_AA_b > 0 || num_BB_a > 0) {
        int min = (num_AB_ab / 2) > num_AA_b ? num_AA_b : (num_AB_ab / 2);
        min = min > num_BB_a ? num_BB_a : min;
        if (min >= 0) {
            M += min;
            num_AB_ab -= 2 * min;
            num_AA_b -= min;
            num_BB_a -= min;
        }
    }
    // M 2AB_ba + AA_a + BB_b
    if (num_AB_ba > 0 || num_AA_a > 0 || num_BB_b > 0) {
        int min = (num_AB_ba / 2) > num_AA_a ? num_AA_a : (num_AB_ba / 2);
        min = min > num_BB_b ? num_BB_b : min;
        if (min >= 0) {
            M += min;
            num_AB_ba -= 2 * min;
            num_AA_a -= min;
            num_BB_b -= min;
        }
    }
    // N AB_ab + AA_b + BB_a 
    if (num_AB_ab > 0 || num_AA_b > 0 || num_BB_a > 0) {
        int min = num_AB_ab > num_AA_b ? num_AA_b : num_AB_ab;
        min = min > num_BB_a ? num_BB_a : min;
        if (min >= 0) {
            N += min;
            num_AB_ab -= min;
            num_AA_b -= min;
            num_BB_a -= min;
        }
    }
    // N AB_ba + AA_a + BB_b
    if (num_AB_ba > 0 || num_AA_a > 0 || num_BB_b > 0) {
        int min = num_AB_ba > num_AA_a ? num_AA_a : num_AB_ba;
        min = min > num_BB_b ? num_BB_b : min;
        if (min >= 0) {
            N += min;
            num_AB_ba -= min;
            num_AA_a -= min;
            num_BB_b -= min;
        }
    }
    // N 2AB_ab + AA_b
    if (num_AB_ab > 0 || num_AA_b > 0) {
        int min = (num_AB_ab / 2) > num_AA_b ? num_AA_b : (num_AB_ab / 2);
        if (min >= 0) {
            N += min;
            num_AB_ab -= 2 * min;
            num_AA_b -= min;
        }
    }
    // N 2AB_ab + BB_a  
    if (num_AB_ab > 0 || num_BB_a > 0) {
        int min = (num_AB_ab / 2) > num_BB_a ? num_BB_a : (num_AB_ab / 2);
        if (min >= 0) {
            N += min;
            num_AB_ab -= 2 * min;
            num_BB_a -= min;
        }
    }
    // N 2AB_ba + AA_a 
    if (num_AB_ba > 0 || num_AA_a > 0) {
        int min = (num_AB_ba / 2) > num_AA_a ? num_AA_a : (num_AB_ba / 2);
        if (min >= 0) {
            N += min;
            num_AB_ba -= 2 * min;
            num_AA_a -= min;
        }
    }
    // N 2AB_ba + BB_b 
    if (num_AB_ba > 0 || num_BB_b > 0) {
        int min = (num_AB_ba / 2) > num_BB_b ? num_BB_b : (num_AB_ba / 2);
        if (min >= 0) {
            N += min;
            num_AB_ba -= 2 * min;
            num_BB_b -= min;
        }
    }

    int dcj_distance = num_shared_genes - num_cycle - (num_AB + num_BA) / 2;
    int indel_distance = sum_lambda - (2 * P + 3 * Q + 2 * T + S + 2 * M + N);
    dist_log.close();

    return std::make_pair(dcj_distance, indel_distance);
}

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "Usage: ./distance <first_genome> <second_genome> <out_file>" << std::endl
                  << "Genome in basic grimm format" << std::endl;
	    if (argc == 2 && std::string(argv[1]) == "--help") {
		    return 0;
    	}
	    return 1;
    }

    IO input;
    auto first_genome = input.ImportGenome(argv[1]);
    auto second_genome = input.ImportGenome(argv[2]);

    auto result = Distance(first_genome, second_genome); 

    std::ofstream stream_out(argv[3]);
    stream_out << result.first << " " << result.second << std::endl;
    stream_out.close();
 
    return 0;
}

