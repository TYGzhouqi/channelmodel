#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019, 2020 Johannes Demel.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
import scipy.constants as spc
import scipy.special as sps


class ChannelCoherence(object):
    """ChannelCoherence

     用这个来形成通道实现之间的连贯感。
    关于它背后的理论，请参考Jakes和Rappaport。
    carrier_freq: 确定相干性可能消失后的距离。
    velocity: 用来将时间delta转换为距离delta。
    """

    def __init__(self, carrier_freq, velocity):
        self._carrier_freq = carrier_freq
        self._velocity = velocity
        self._time2distance_factor = (self._velocity * self._carrier_freq /
                                      spc.speed_of_light)

    def state(self):
        d = {
            'freq': self._carrier_freq,
            'velocity': self._velocity
        }
        return d

    def __str__(self):
        s = type(self).__name__ + '('
        s += 'freq={}'.format(self._carrier_freq)
        s += 'velocity={}'.format(self._velocity)
        return s + ')'

    def coherence_distance(self, distance_delta):
        raise NotImplementedError('Method must be implemented by child class!')

    def coherence_time(self, time_delta):
        return self.get_covariance_time(time_delta)

    def get_covariance_time(self, time_delta):
        distance_delta = time_delta * self._time2distance_factor
        return self.get_covariance_distance(distance_delta)

    def get_covariance_distance(self, distance_delta):
        return self.coherence_distance(distance_delta)


class ChannelCoherenceRappaport(ChannelCoherence):
    def __init__(self, carrier_freq, velocity):
        super(ChannelCoherenceRappaport, self).__init__(carrier_freq, velocity)

    def coherence_distance(self, distance_delta):
        '''
        Just the Ez-case from Rappaport.
        This implies omnidirectional antennae.
        It's a nice approximation.
        '''
        return np.exp(-23. * (distance_delta ** 2))


class ChannelCoherenceJakes(ChannelCoherence):
    def __init__(self, carrier_freq, velocity):
        super(ChannelCoherenceJakes, self).__init__(carrier_freq, velocity)

    def coherence_distance(self, distance_delta):
        '''
        Just the Ez-case from Rappaport.
        This implies omnidirectional antennae.
        It's a nice approximation.
        '''
        return sps.j0(2. * np.pi * distance_delta) ** 2
