/** @file Model.h
 *
 * Copyright (c) 2024 IACE
 */
#ifndef MODEL_H
#define MODEL_H

#include <comm/min.h>
#include <core/experiment.h>
#include <utils/later.h>
#include <comm/series.h>

#include "support.h"
#include "OneMassOscillator.h"
#include "TrajType.h"


struct Model {
    enum Config {TRAJ};

    OneMassOscillator oscillator {
        .input = (Later<OneMassOscillator::Input>) trajType.out,
    };

    TrajType trajType;

    FrameRegistry &fr {support.min.reg};
    Min::Out &out {support.min.out};

    void reset(uint32_t) {
        oscillator.reset();
        trajType.reset();
    }

    void init() {
        // reset
        e.onEvent(e.INIT).call(*this, &Model::reset);

        e.during(e.RUN).every(1, oscillator, &OneMassOscillator::tick);

        // timesteps
        e.during(e.RUN).every(2, trajType, &TrajType::step);

        e.during(e.RUN).every(20, *this, &Model::sendModelData);
        e.during(e.RUN).every(20, *this, &Model::sendTrajData);

        fr.setHandler(10, *this, &Model::setModelData);
        fr.setHandler(11, *this, &Model::setModelParams);
        fr.setHandler(20, *this, &Model::setTrajType);
        fr.setHandler(21, trajType, &TrajType::setData);
    }

    void sendModelData(uint32_t time, uint32_t) {
        Frame f{15};
        f.pack(time);
        f.pack(oscillator.state(0));
        f.pack(oscillator.state(1));
        f.pack(oscillator.in);
        out.push(f);
    }

    void setModelParams(Frame &f) {
        oscillator.params(0) = f.unpack<double>();
        oscillator.params(1) = f.unpack<double>();
        oscillator.params(2) = f.unpack<double>();
    }

    void sendTrajData(uint32_t time, uint32_t) {
        Frame f{25};
        f.pack(time);
        f.pack(trajType.des[0]);
        f.pack(trajType.des[1]);
        out.push(f);
    }

    void setModelData(Frame &f) {
        auto config = f.unpack<uint8_t>();

        switch (config) {
            case Config::TRAJ: {
                oscillator.input = (Later<OneMassOscillator::Input>) trajType.out;
                break;
            }
        }
    }

    void setTrajType(Frame &f) {
        trajType.mkType(f.unpack<TrajType::Type>());
    }
};

#endif //MODEL_H
