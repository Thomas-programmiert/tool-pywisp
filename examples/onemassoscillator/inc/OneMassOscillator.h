/** @file OneMassOscillator.h
 *
 * Copyright (c) 2024 IACE
 */
#ifndef ONEMASSOSCILLATOR_H
#define ONEMASSOSCILLATOR_H

#include <utils/later.h>
#include <Eigen/Dense>

struct OneMassOscillator {
    using State = Eigen::Matrix<double, 2, 1>;
    State state{};

    using Parameters = Eigen::Matrix<double, 3, 1>;
    Parameters params{1.0, 0.1, 0.5};

    using Input = double;
    Later<Input> input;
    double in;

    void tick(uint32_t time, uint32_t dt) {
        this->in = input.get();
        auto u = this->in;
        setInput(u);

        updateState(time, dt);
    };

    void reset();
    void setInput(double);
    void updateState(uint32_t time, uint32_t dt);
};

#endif //ONEMASSOSCILLATOR_H
