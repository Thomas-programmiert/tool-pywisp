/** @file sim.cpp
 *
 * Copyright (c) 2024 IACE
 */
#include <core/experiment.h>
#include <sys/comm.h>
#include <sys/sim.h>
#include "model.h"
#include "OneMassOscillator.h"
#include "LinOneMassOscillator.h"

TTY tty{"/dev/tty"};
UDP udp{"127.0.0.1", 45670};
OneMassOscillator::Input u;

void OneMassOscillator::updateState(uint32_t time, uint32_t dt_ms) {
    double dt = dt_ms / 1000.;

    state = state + dt * LinOneMassOscillator::step(state, u, params);

    k.log.print("%g, %g, %g, %g\n",
                state[0], state[1],
                u,
                dt
    );
}

void OneMassOscillator::reset() {
    state = OneMassOscillator::State{0.5, 0.1};
}

void OneMassOscillator::setInput(double val) {
    u = val;
}

Support::Support() : min{.in = udp, .out = udp }{}

void Support::init() {
    e.onEvent(e.STOP).call([](uint32_t) {
        u = OneMassOscillator::Input{};
    });

    e.onEvent(e.INIT).call([](uint32_t) {
        k.log.print("starting simulation");
    });
}

Kernel k;
Support support;
Experiment e{&support.min.reg};

int main(int argc, char *argv[]) {
    k.initLog(tty);
    k.setTimeStep(getSimTimeStep(argc, argv));
    k.every(1, support.min, &Min::poll);
    support.init();

    Model m;
    m.init();
    k.run();
}
