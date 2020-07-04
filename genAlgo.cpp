#include <iostream>
#include <string>
#include <array>
#include <chrono>
#include <random>
using std::string;
using std::cout;
using std::endl;
using namespace std::chrono;

class Individual{
    private:
        std::string genes;
        int fitness;
    public:
        Individual(std::string genes_, int fitness_): genes(genes_), fitness(fitness_){}
        std::string get_genes(){
            return genes;
        }
        int get_fitness(){
            return fitness;
        }
        void set_genes(std::string genes_){
            genes = genes_;
        }
        void set_fitness(int fitness_){
            fitness = fitness_;
        }
};

int hamming_dist(std::string first, std::string second){
    int count = 0;
    for(int i =0; i < first.size(); i++){
        if(first[i] != second[i])
            count++;
    }
    return count;
}

string create_genes(int SIZE){
    string alphabet ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ");
    string genes;
    std::random_device rd;
    for(int i = 0; i < SIZE; i++){
        genes += alphabet[rd()%alphabet.size()];
    }
    return genes;
}

Individual* get_fittest(Individual* population[], int size){
    int best_index = 0;
    for(int i = 1; i < size; i++){
        if(population[i]->get_fitness() < population[best_index]->get_fitness()){
            best_index = i;
        }
    }
    return population[best_index];
}

Individual** create_population(int SIZE, string target){
    Individual** population = new Individual*[SIZE];
    for(int i = 0; i < SIZE; i++){
        population[i] = new Individual(create_genes(target.size()),0);
        population[i]->set_fitness(hamming_dist(population[i]->get_genes(), target));
    }
    return population;
}

string mutate_genes(string genes){
    std::random_device rd;
    string alphabet ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ");
    for(int i = 0; i < genes.size(); i++){
        if(rd()%1000 < 10){
            string mutaition (1,alphabet[rd()%alphabet.size()]);
            genes.replace(i,1,mutaition);
        }
    }
    return genes;
}

Individual* tournament(Individual* population[], int size){
    Individual** tourny_pop = new Individual*[5];
    std::random_device rd;
    for(int i = 0; i < 5; i++){
        tourny_pop[i] = population[rd()%size];
    }
    return get_fittest(tourny_pop, 5);
}

Individual* cross_over(Individual* parent1, Individual* parent2, string target){
    string new_genes;
    std::random_device rd;
    for(int i = 0; i < parent1->get_genes().size(); i++){
        if(rd()%2 == 0){
            new_genes += parent1->get_genes()[i];
        }else{
            new_genes += parent2->get_genes()[i];
        }
    }
    return new Individual(new_genes,hamming_dist(new_genes, target));
}

void gen_algo(string target, int SIZE){

    int generations = 0;
    Individual** population = create_population(SIZE,target);
    Individual* fittest = get_fittest(population, SIZE);
    do{
        Individual** new_pop = new Individual*[SIZE];
        fittest = get_fittest(population, SIZE);
        new_pop[0] = fittest;
        
        for(int i = 1; i < SIZE; i++){
            Individual* child = cross_over(tournament(population, SIZE),tournament(population, SIZE), target);
            child->set_genes(mutate_genes(child->get_genes()));
            child->set_fitness(hamming_dist(child->get_genes(), target));
            new_pop[i] = child;
        }
        // cout << fittest->get_genes() << endl;
        population = new_pop;
        generations++;
    }while(fittest->get_fitness() != 0);

    cout << fittest->get_genes() << endl;
    cout << "Took " << generations << " generations" << endl;
}

int main(int argc, char** argv){
   
    if(argc < 3){
        cout << "Usage\ngenalgo.c <int> <string> \n";
        return 0;
    }

    int SIZE = atoi(argv[1]);
    string target (argv[2]);

    auto start = high_resolution_clock::now();

    gen_algo(target,SIZE);

    auto finish = high_resolution_clock::now();
    duration<double> elapsed = finish - start;
    std::cout << "Elapsed time: " << elapsed.count() << " s\n";


    return 0;
}
