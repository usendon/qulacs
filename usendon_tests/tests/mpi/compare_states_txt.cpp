#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <complex>
#include <string>
#include <cmath>

using cd = std::complex<double>;
const double TOL = 1e-3;

bool parseLine(const std::string &line, cd &out) {
    size_t colon = line.find(":");
    if (colon == std::string::npos) return false;

    std::string val = line.substr(colon + 1);

    double real = 0.0, imag = 0.0;
    char sign;

    std::stringstream ss(val);
    ss >> real >> sign >> imag;

    if (sign == '-') imag = -imag;

    out = cd(real, imag);
    return true;
}

bool areEqual(const std::vector<cd> &a, const std::vector<cd> &b) {
    if (a.size() != b.size()) return false;

    for (size_t i = 0; i < a.size(); i++) {
        if (std::abs(a[i] - b[i]) > TOL) {
            return false;
        }
    }
    return true;
}

int main() {
    std::ifstream file("comparar_estados.txt");
    if (!file) {
        std::cerr << "Error al abrir archivo\n";
        return 1;
    }

    std::string line;
    std::string currentGate = "";

    std::vector<cd> multi, single;

    enum Mode { NONE, MULTI, SINGLE };
    Mode mode = NONE;

    auto flush = [&]() {
        if (!currentGate.empty()) {
            if (areEqual(multi, single)) {
                std::cout << currentGate << " -> IGUALES\n";
            } else {
                std::cout << currentGate << " -> DIFERENTES\n";
            }
        }
        multi.clear();
        single.clear();
    };

    while (std::getline(file, line)) {

        // Nuevo bloque
        if (line.find("ECR gate") != std::string::npos) {
            flush(); // cerrar el anterior

            currentGate = line;
            mode = NONE;
            continue;
        }

        if (line.find("multi-cpu") != std::string::npos) {
            mode = MULTI;
            continue;
        }

        if (line.find("single cpu") != std::string::npos) {
            mode = SINGLE;
            continue;
        }

        if (line.find("F|") != std::string::npos) {
            cd amp;
            if (parseLine(line, amp)) {
                if (mode == MULTI) multi.push_back(amp);
                else if (mode == SINGLE) single.push_back(amp);
            }
        }
    }

    // último bloque
    flush();

    return 0;
}