# -*- coding: utf-8 -*-

"""
This file contains the Qudi Predefined Methods for sequence generator

Qudi is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Qudi is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Qudi. If not, see <http://www.gnu.org/licenses/>.

Copyright (c) the Qudi Developers. See the COPYRIGHT.txt file at the
top-level directory of this distribution and at <https://github.com/Ulm-IQO/qudi/>
"""

import numpy as np
from logic.pulsed.pulse_objects import PulseBlock, PulseBlockEnsemble, PulseSequence
from logic.pulsed.pulse_objects import PredefinedGeneratorBase

"""
General Pulse Creation Procedure:
=================================
- Create at first each PulseBlockElement object
- add all PulseBlockElement object to a list and combine them to a
  PulseBlock object.
- Create all needed PulseBlock object with that idea, that means
  PulseBlockElement objects which are grouped to PulseBlock objects.
- Create from the PulseBlock objects a PulseBlockEnsemble object.
- If needed and if possible, combine the created PulseBlockEnsemble objects
  to the highest instance together in a PulseSequence object.
"""


class BasicPredefinedGenerator(PredefinedGeneratorBase):
    """

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    ################################################################################################
    #                             Generation methods for waveforms                                 #
    ################################################################################################
    def generate_laser_on(self, name='laser_on', length=3.0e-6):
        """ Generates Laser on.

        @param str name: Name of the PulseBlockEnsemble
        @param float length: laser duration in seconds

        @return object: the generated PulseBlockEnsemble object.
        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # create the laser element
        laser_element = self._get_laser_element(length=length, increment=0)
        # Create block and append to created_blocks list
        laser_block = PulseBlock(name=name)
        laser_block.append(laser_element)
        created_blocks.append(laser_block)
        # Create block ensemble and append to created_ensembles list
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((laser_block.name, 0))
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_laser_mw_on(self, name='laser_mw_on', length=3.0e-6):
        """ General generation method for laser on and microwave on generation.

        @param string name: Name of the PulseBlockEnsemble to be generated
        @param float length: Length of the PulseBlockEnsemble in seconds

        @return object: the generated PulseBlockEnsemble object.
        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # create the laser_mw element
        laser_mw_element = self._get_mw_laser_element(length=length,
                                                      increment=0,
                                                      amp=self.microwave_amplitude,
                                                      freq=self.microwave_frequency,
                                                      phase=0)
        # Create block and append to created_blocks list
        laser_mw_block = PulseBlock(name=name)
        laser_mw_block.append(laser_mw_element)
        created_blocks.append(laser_mw_block)
        # Create block ensemble and append to created_ensembles list
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((laser_mw_block.name, 0))
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_two_digital_high(self, name='digital_high', length=3.0e-6, digital_channel1='d_ch1', digital_channel2='d_ch1'):
        """ General generation method for laser on and microwave on generation.

        @param string name: Name of the PulseBlockEnsemble to be generated
        @param float length: Length of the PulseBlockEnsemble in seconds

        @return object: the generated PulseBlockEnsemble object.
        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        digital_channels = list([digital_channel1, digital_channel2])
        # create the laser_mw element
        trigger_element = self._get_trigger_element(length =length,
                                                    increment=0,
                                                    channels=list(digital_channels))

        # Create block and append to created_blocks list
        laser_mw_block = PulseBlock(name=name)
        laser_mw_block.append(trigger_element)
        created_blocks.append(laser_mw_block)
        # Create block ensemble and append to created_ensembles list
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((laser_mw_block.name, 0))
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_idle(self, name='idle', length=3.0e-6):
        """ Generate just a simple idle ensemble.

        @param str name: Name of the PulseBlockEnsemble to be generated
        @param float length: Length of the PulseBlockEnsemble in seconds

        @return object: the generated PulseBlockEnsemble object.
        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # create the laser_mw element
        idle_element = self._get_idle_element(length=length, increment=0)
        # Create block and append to created_blocks list
        idle_block = PulseBlock(name=name)
        idle_block.append(idle_element)
        created_blocks.append(idle_block)
        # Create block ensemble and append to created_ensembles list
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((idle_block.name, 0))
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_rabi(self, name='rabi', tau_start=10.0e-9, tau_step=10.0e-9, num_of_points=50):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        tau_array = tau_start + np.arange(num_of_points) * tau_step

        # create the laser_mw element
        mw_element = self._get_mw_element(length=tau_start,
                                          increment=tau_step,
                                          amp=self.microwave_amplitude,
                                          freq=self.microwave_frequency,
                                          phase=0)
        waiting_element = self._get_idle_element(length=self.wait_time,
                                                 increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length,
                                                     increment=0)
        delay_element = self._get_delay_gate_element()

        # Create block and append to created_blocks list
        rabi_block = PulseBlock(name=name)
        rabi_block.append(mw_element)
        rabi_block.append(laser_element)
        rabi_block.append(delay_element)
        rabi_block.append(waiting_element)
        created_blocks.append(rabi_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((rabi_block.name, num_of_points - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = False
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = tau_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = num_of_points
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # Append ensemble to created_ensembles list
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    # *************************************************************************************************
    # ************************************************************************************************
    # Dec.5 I changed the read next cycle delay to from 1e-6 to 900e-9.
    # Added step size decrease of read next cycle in each loop
    def generate_FRS(self, name='FRS', ini_short=10.0e-9, ini_long=3.0e-6,
                     ini_mic_delay1=1.0e-6,
                     microwave_start=10.0e-9,
                     microwave_step=10.0e-9, mic_read_delay=700.0e-9, readout=300.0e-9,
                     read_nextcycle_delay=900.0e-9, read_nextcycle_delay_step=10.0e-9, num_of_cycles=25,
                     laser_channel='d_ch1',
                     mw_channel='d_ch2', time_tagger_channel='d_ch3'):
        ini_mic_delay_start = 300.0e-9
        ini_mic_delay_step = -10.0e-9
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()
        # get ini_mic_delay and microwave array for measurement ticks
        # tau_array = tau_start + np.arange(num_of_cycles) * tau_step
        ini_mic_delay_array = ini_mic_delay_start + np.arange(num_of_cycles) * ini_mic_delay_step
        microwave_array = microwave_start + np.arange(num_of_cycles) * microwave_step
        i_array = np.arange(num_of_cycles - 1)

        # Create block and append to created_blocks list
        rabi_block = PulseBlock(name=name)

        # first two rows
        readout_element = self._get_trigger_element(length=readout, increment=0, channels=laser_channel)
        rabi_block.append(readout_element)

        read_nextcycle_delay_element = self._get_idle_element(length=read_nextcycle_delay, increment=0)
        rabi_block.append(read_nextcycle_delay_element)

        # TODO: CHOOSE TO START TIME TAGGER BEFORE OR CHOOSE TO ADD IT IN PULSE BLOCK MANUALLY
        # start_time_tagger_element = self._get_trigger_element(length=1e-9, increment=0, channels=time_tagger_channel)
        # rabi_block.append(start_time_tagger_element)

        # cycle starts
        for i in i_array:
            if i == 0:
                ini_short_element = self._get_trigger_element(length=ini_short, increment=0,
                                                              channels=[laser_channel, time_tagger_channel])
            else:
                ini_short_element = self._get_trigger_element(length=ini_short, increment=0, channels=laser_channel)
            rabi_block.append(ini_short_element)
            ini_long_element = self._get_trigger_element(length=ini_long, increment=0, channels=laser_channel)
            rabi_block.append(ini_long_element)  # initialization

            ini_mic_delay_element1 = self._get_idle_element(length=ini_mic_delay1, increment=0)
            rabi_block.append(ini_mic_delay_element1)
            ini_mic_delay_element = self._get_idle_element(length=ini_mic_delay_array[i], increment=0)
            rabi_block.append(ini_mic_delay_element)  # initialization_microwave delay

            mw_element = self._get_trigger_element(length=microwave_array[i], increment=0, channels=mw_channel)
            rabi_block.append(mw_element)  # microwave

            mic_read_delay_element = self._get_idle_element(length=mic_read_delay, increment=0)
            rabi_block.append(mic_read_delay_element)  # microwave_readout delay

            readout_element = self._get_trigger_element(length=readout, increment=0, channels=laser_channel)
            rabi_block.append(readout_element)  # readout

            read_nextcycle_delay_element = \
                self._get_idle_element(length=read_nextcycle_delay - (i + 1) * read_nextcycle_delay_step,
                                       increment=0)
            rabi_block.append(read_nextcycle_delay_element)  # readout_next-cycle delay

        # last cycle
        ini_short_element = self._get_trigger_element(length=ini_short, increment=0, channels=laser_channel)
        rabi_block.append(ini_short_element)
        ini_long_element = self._get_trigger_element(length=ini_long, increment=0, channels=laser_channel)
        rabi_block.append(ini_long_element)  # initialization

        ini_mic_delay_element1 = self._get_idle_element(length=ini_mic_delay1, increment=0)
        rabi_block.append(ini_mic_delay_element1)
        ini_mic_delay_element = self._get_idle_element(length=ini_mic_delay_array[i], increment=0)
        rabi_block.append(ini_mic_delay_element)  # initialization_microwave delay

        mw_element = self._get_trigger_element(length=microwave_array[i], increment=0, channels=mw_channel)
        rabi_block.append(mw_element)  # microwave

        mic_read_delay_element = self._get_idle_element(length=mic_read_delay, increment=0)
        rabi_block.append(mic_read_delay_element)  # microwave_readout delay

        # laser_element = self._get_laser_gate_element(length=self.laser_length,
        #                                             increment=0)
        # delay_element = self._get_delay_gate_element()
        # rabi_block.append(laser_element)
        # rabi_block.append(delay_element)

        created_blocks.append(rabi_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((rabi_block.name, num_of_cycles - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = False
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable1'] = ini_mic_delay_array
        block_ensemble.measurement_information['controlled_variable2'] = microwave_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = num_of_cycles
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # Append ensemble to created_ensembles list
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    # *************************************************************************************************
    # *************************************************************************************************

    # *************************************************************************************************
    # *************************************************************************************************
    # June 4, 2021. Sequence of t1 pulsing made by editing t1 pulsing method, edited by Andrew
    def generate_t1_prototype_one(self, name='T1_prototype_one', ini_short=10e-9, ini_long=3e-6, ini_micro_delay=1e-6,
                                  microwave=75e-9, mic_read_delay_start=1e-3, mic_read_delay_step=5e-3,
                                  mic_read_delay_first_step=4e-3, readout=300e-9,
                                  read_next_delay_start=29e-3, read_next_delay_first_step=-4e-3,
                                  read_next_delay_step=-5e-3,
                                  num_of_cycles=4, laser_channel='d_ch1', mw_channel='d_ch2',
                                  time_tagger_channel='d_ch3', alternating=False):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        mic_read_delay_array = mic_read_delay_start + np.arange(num_of_cycles) * mic_read_delay_step
        read_next_delay_array = read_next_delay_start + np.arange(num_of_cycles) * read_next_delay_step
        i_array = np.arange(num_of_cycles - 1)

        # create the elements

        t1_block = PulseBlock(name=name)

        # first two rows
        readout_element = self._get_trigger_element(length=readout, increment=0, channels=laser_channel)
        t1_block.append(readout_element)

        read_next_delay_element = self._get_idle_element(length=read_next_delay_array[num_of_cycles - 1] -
                                                                (read_next_delay_step - read_next_delay_first_step),
                                                         increment=0)
        t1_block.append(read_next_delay_element)

        # cycle starts
        for i in i_array:
            if i == 0:
                ini_short_element = self._get_trigger_element(length=ini_short, increment=0,
                                                              channels=[laser_channel, time_tagger_channel])
            else:
                ini_short_element = self._get_trigger_element(length=ini_short, increment=0, channels=laser_channel)
            t1_block.append(ini_short_element)
            ini_long_element = self._get_trigger_element(length=ini_long, increment=0, channels=laser_channel)
            t1_block.append(ini_long_element)

            ini_micro_delay_element = self._get_idle_element(length=ini_micro_delay, increment=0)
            t1_block.append(ini_micro_delay_element)

            microwave_element = self._get_trigger_element(length=microwave, increment=0, channels=mw_channel)
            t1_block.append(microwave_element)

            if i == 0:
                mic_read_delay_element = self._get_idle_element(length=mic_read_delay_array[i], increment=0)
            else:
                mic_read_delay_element = self._get_idle_element(length=mic_read_delay_array[i] -
                                                                (mic_read_delay_step - mic_read_delay_first_step),
                                                                increment=0)
            t1_block.append(mic_read_delay_element)

            if i == 0:
                readout_element = self._get_idle_element(length=readout, increment=0)
            else:
                readout_element = self._get_trigger_element(length=readout, increment=0, channels=laser_channel)
            t1_block.append(readout_element)

            if i == 0:
                read_next_delay_element = \
                    self._get_idle_element(length=read_next_delay_array[i], increment=0)
            else:
                read_next_delay_element = self._get_idle_element(length=read_next_delay_array[i] -
                                                                (read_next_delay_step - read_next_delay_first_step),
                                                                 increment=0)
            t1_block.append(read_next_delay_element)

        # last 5 rows
        ini_short_element = self._get_trigger_element(length=ini_short, increment=0, channels=laser_channel)
        t1_block.append(ini_short_element)
        ini_long_element = self._get_trigger_element(length=ini_long, increment=0, channels=laser_channel)
        t1_block.append(ini_long_element)

        ini_micro_delay_element = self._get_idle_element(length=ini_micro_delay, increment=0)
        t1_block.append(ini_micro_delay_element)

        microwave_element = self._get_trigger_element(length=microwave, increment=0, channels=mw_channel)
        t1_block.append(microwave_element)

        mic_read_delay_element = \
            self._get_idle_element(length=mic_read_delay_array[num_of_cycles - 1] -
                                          (mic_read_delay_step - mic_read_delay_first_step), increment=0)
        t1_block.append(mic_read_delay_element)

        created_blocks.append(t1_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((t1_block.name, num_of_cycles - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        number_of_lasers = 2 * num_of_cycles if alternating else num_of_cycles
        block_ensemble.measurement_information['alternating'] = alternating
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable1'] = mic_read_delay_array
        block_ensemble.measurement_information['controlled_variable2'] = read_next_delay_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = number_of_lasers
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)
        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences
    # *************************************************************************************************
    # *************************************************************************************************

    # *************************************************************************************************
    # *************************************************************************************************
    # edited by Andrew Tong on Jan.12th
    def generate_RamseyMach1(self, name='RamseyMach1', step_1=300.0e-9, step_2=1.99e-6,
                             step_3=10.0e-9, step_4=3.0e-6, step_5=700.0e-9, step_6=75.0e-9, step_7=10.0e-9,
                             step_8=75.0e-9, step_9=700.0e-9, step_10=300.0e-9, step_11=2.0e-6,
                             positive_step=10.0e-9, negative_step=-10.0e-9,
                             num_of_cycles=100,
                             laser_channel='d_ch1',
                             mw_channel='d_ch2', time_tagger_channel='d_ch3'):

        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        i_array = np.arange(num_of_cycles)

        # Create block and append to created_blocks list
        rabi_block = PulseBlock(name=name)

        # TODO: CHOOSE TO START TIME TAGGER BEFORE OR CHOOSE TO ADD IT IN PULSE BLOCK MANUALLY

        # first steps
        s1 = self._get_trigger_element(length=step_1, increment=0, channels=laser_channel)
        rabi_block.append(s1)
        s2 = self._get_idle_element(length=step_2, increment=0)
        rabi_block.append(s2)

        # cycle starts
        for i in i_array:

            if i == 0:
                s3 = self._get_trigger_element(length=step_3, increment=0,
                                               channels=[laser_channel, time_tagger_channel])
            else:
                s3 = self._get_trigger_element(length=step_3, increment=0,
                                               channels=laser_channel)
            rabi_block.append(s3)

            s4 = self._get_trigger_element(length=step_4, increment=0, channels=laser_channel)
            rabi_block.append(s4)

            s5 = self._get_idle_element(length=step_5, increment=0)
            rabi_block.append(s5)

            s6 = self._get_trigger_element(length=step_6, increment=0, channels=mw_channel)
            rabi_block.append(s6)

            s7 = self._get_idle_element(length=step_7 + positive_step * i, increment=0)
            rabi_block.append(s7)

            s8 = self._get_trigger_element(length=step_8, increment=0, channels=mw_channel)
            rabi_block.append(s8)

            s9 = self._get_idle_element(length=step_9, increment=0)
            rabi_block.append(s9)

            s10 = self._get_trigger_element(length=step_10, increment=0, channels=laser_channel)
            rabi_block.append(s10)

            if i == 0:
                s11 = self._get_idle_element(length=step_11, increment=0)
            else:
                s11 = self._get_idle_element(length=step_11 + negative_step * i,
                                             increment=0)
            rabi_block.append(s11)

        created_blocks.append(rabi_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((rabi_block.name, num_of_cycles - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = False
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        # block_ensemble.measurement_information['controlled_variable1'] = ini_mic_delay_array
        # block_ensemble.measurement_information['controlled_variable2'] = microwave_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = num_of_cycles
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # Append ensemble to created_ensembles list
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences
    # *************************************************************************************************
    # *************************************************************************************************

    # *************************************************************************************************
    # *************************************************************************************************
    # edited by Andrew on Jan.12th
    def generate_HahnEchoMach1(self, name='HahnEchoMach1', step_1=300.0e-9, step_2=99.98e-6,
                               step_3=10.0e-9, step_4=3.0e-6, step_5=700.0e-9, step_6=75.0e-9, step_7=10.0e-9,
                               step_8=150.0e-9, step_9=10.0e-9, step_10=75.0e-9, step_11=700.0e-9,
                               step_12=300.0e-9, step_13=100.0e-6,
                               positive_step=10.0e-9, negative_step=-10.0e-9,
                               num_of_cycles=100,
                               laser_channel='d_ch1',
                               mw_channel='d_ch2', time_tagger_channel='d_ch3'):

        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        i_array = np.arange(num_of_cycles)

        # Create block and append to created_blocks list
        rabi_block = PulseBlock(name=name)

        # TODO: CHOOSE TO START TIME TAGGER BEFORE OR CHOOSE TO ADD IT IN PULSE BLOCK MANUALLY

        # first steps
        s1 = self._get_trigger_element(length=step_1, increment=0, channels=laser_channel)
        rabi_block.append(s1)
        s2 = self._get_idle_element(length=step_2, increment=0)
        rabi_block.append(s2)

        # cycle starts
        for i in i_array:

            if i == 0:
                s3 = self._get_trigger_element(length=step_3, increment=0,
                                               channels=[laser_channel, time_tagger_channel])
            else:
                s3 = self._get_trigger_element(length=step_3, increment=0,
                                               channels=laser_channel)
            rabi_block.append(s3)

            s4 = self._get_trigger_element(length=step_4, increment=0, channels=laser_channel)
            rabi_block.append(s4)

            s5 = self._get_idle_element(length=step_5, increment=0)
            rabi_block.append(s5)

            s6 = self._get_trigger_element(length=step_6, increment=0, channels=mw_channel)
            rabi_block.append(s6)

            s7 = self._get_idle_element(length=step_7 + positive_step * i, increment=0)
            rabi_block.append(s7)

            s8 = self._get_trigger_element(length=step_8, increment=0, channels=mw_channel)
            rabi_block.append(s8)

            s9 = self._get_idle_element(length=step_9 + positive_step * i, increment=0)
            rabi_block.append(s9)

            s10 = self._get_trigger_element(length=step_10, increment=0, channels=mw_channel)
            rabi_block.append(s10)

            s11 = self._get_idle_element(length=step_11, increment=0)
            rabi_block.append(s11)

            s12 = self._get_trigger_element(length=step_12, increment=0, channels=laser_channel)
            rabi_block.append(s12)

            if i == 0:
                s13 = self._get_idle_element(length=step_13, increment=0)
            else:
                s13 = self._get_idle_element(length=step_13 + negative_step * i, increment=0)
            rabi_block.append(s13)

        created_blocks.append(rabi_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((rabi_block.name, num_of_cycles - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = False
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        # block_ensemble.measurement_information['controlled_variable1'] = ini_mic_delay_array
        # block_ensemble.measurement_information['controlled_variable2'] = microwave_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = num_of_cycles
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # Append ensemble to created_ensembles list
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences
    # *************************************************************************************************
    # *************************************************************************************************

    # *************************************************************************************************
    # *************************************************************************************************
    # edited by Andrew on Jan.13th
    def generate_Rabipnew(self, name='Rabipnew', step_1=300.0e-9, step_2=2.98e-6,
                          step_3=10.0e-9, step_4=3.0e-6, step_5=1.0e-6, step_6=10.0e-9, step_7=500.0e-9,
                          step_8=300.0e-9, step_9=3.0e-6,
                          positive_step=10.0e-9, negative_step=-10.0e-9,
                          num_of_cycles=100,
                          laser_channel='d_ch1',
                          mw_channel='d_ch2', time_tagger_channel='d_ch3'):

        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        i_array = np.arange(num_of_cycles)

        # Create block and append to created_blocks list
        rabi_block = PulseBlock(name=name)

        # TODO: CHOOSE TO START TIME TAGGER BEFORE OR CHOOSE TO ADD IT IN PULSE BLOCK MANUALLY

        # first steps
        s1 = self._get_trigger_element(length=step_1, increment=0, channels=laser_channel)
        rabi_block.append(s1)
        s2 = self._get_idle_element(length=step_2, increment=0)
        rabi_block.append(s2)

        # cycle starts
        for i in i_array:

            if i == 0:
                s3 = self._get_trigger_element(length=step_3, increment=0,
                                               channels=[laser_channel, time_tagger_channel])
            else:
                s3 = self._get_trigger_element(length=step_3, increment=0,
                                               channels=laser_channel)
            rabi_block.append(s3)

            s4 = self._get_trigger_element(length=step_4, increment=0, channels=laser_channel)
            rabi_block.append(s4)

            s5 = self._get_idle_element(length=step_5, increment=0)
            rabi_block.append(s5)

            s6 = self._get_trigger_element(length=step_6 + positive_step * i, increment=0, channels=mw_channel)
            rabi_block.append(s6)

            s7 = self._get_idle_element(length=step_7, increment=0)
            rabi_block.append(s7)

            s8 = self._get_trigger_element(length=step_8, increment=0, channels=laser_channel)
            rabi_block.append(s8)

            if i == 0:
                s9 = self._get_idle_element(length=step_9, increment=0)
            else:
                s9 = self._get_idle_element(length=step_9 + negative_step * i, increment=0)
            rabi_block.append(s9)

        created_blocks.append(rabi_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((rabi_block.name, num_of_cycles - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = False
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        # block_ensemble.measurement_information['controlled_variable1'] = ini_mic_delay_array
        # block_ensemble.measurement_information['controlled_variable2'] = microwave_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = num_of_cycles
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # Append ensemble to created_ensembles list
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences
    # *************************************************************************************************
    # *************************************************************************************************

    # *************************************************************************************************
    # *************************************************************************************************
    # edited by Andrew on Jun.15th
    def generate_RSQ(self, name='RSQ', step_1=10.0e-9, step_2=3.0e-6,
                     step_3=300.0e-9, step_4=100.0e-9, step_5=10.0e-9, step_6=100.0e-9, step_7=300.0e-9,
                     step_8=300.0e-9, step_9=1.29e-6,
                     positive_step=10.0e-9, negative_step=-10.0e-9,
                     num_of_cycles=100,
                     laser_channel='d_ch1',
                     mw_channel='d_ch2', time_tagger_channel='d_ch3'):

        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        i_array = np.arange(num_of_cycles)

        # Create block and append to created_blocks list
        rabi_block = PulseBlock(name=name)

        # TODO: CHOOSE TO START TIME TAGGER BEFORE OR CHOOSE TO ADD IT IN PULSE BLOCK MANUALLY

        # cycle starts
        for i in i_array:

            if i == 0:
                s1 = self._get_trigger_element(length=step_1, increment=0,
                                               channels=[laser_channel, time_tagger_channel])
            else:
                s1 = self._get_trigger_element(length=step_1, increment=0,
                                               channels=laser_channel)
            rabi_block.append(s1)

            s2 = self._get_trigger_element(length=step_2, increment=0, channels=laser_channel)
            rabi_block.append(s2)

            s3 = self._get_idle_element(length=step_3, increment=0)
            rabi_block.append(s3)

            s4 = self._get_trigger_element(length=step_4, increment=0, channels=mw_channel)
            rabi_block.append(s4)

            s5 = self._get_idle_element(length=step_5 + positive_step * i, increment=0)
            rabi_block.append(s5)

            s6 = self._get_trigger_element(length=step_6, increment=0, channels=mw_channel)
            rabi_block.append(s6)

            s7 = self._get_idle_element(length=step_7, increment=0)
            rabi_block.append(s7)

            s8 = self._get_trigger_element(length=step_8, increment=0, channels=laser_channel)
            rabi_block.append(s8)

            s9 = self._get_idle_element(length=step_9 + negative_step * i, increment=0)
            rabi_block.append(s9)

        created_blocks.append(rabi_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((rabi_block.name, num_of_cycles - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = False
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        # block_ensemble.measurement_information['controlled_variable1'] = ini_mic_delay_array
        # block_ensemble.measurement_information['controlled_variable2'] = microwave_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = num_of_cycles
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # Append ensemble to created_ensembles list
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences
        # *************************************************************************************************
        # *************************************************************************************************

    # *************************************************************************************************
    # *************************************************************************************************
    # edited by Andrew on Jun.15th
    def generate_HES(self, name='HES', step_1=10.0e-9, step_2=3.0e-6,
                     step_3=300.0e-9, step_4=50.0e-9, step_5=10.0e-9, step_6=100.0e-9, step_7=10.0e-9,
                     step_8=50.0e-9, step_9=300.0e-6, step_10=300.0e-9, step_11=50.28e-6,
                     positive_step=10.0e-9, negative_step=-20.0e-9,
                     num_of_cycles=100,
                     laser_channel='d_ch1',
                     mw_channel='d_ch2', time_tagger_channel='d_ch3'):

        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        i_array = np.arange(num_of_cycles)

        # Create block and append to created_blocks list
        rabi_block = PulseBlock(name=name)

        # TODO: CHOOSE TO START TIME TAGGER BEFORE OR CHOOSE TO ADD IT IN PULSE BLOCK MANUALLY

        # cycle starts
        for i in i_array:

            if i == 0:
                s1 = self._get_trigger_element(length=step_1, increment=0,
                                               channels=[laser_channel, time_tagger_channel])
            else:
                s1 = self._get_trigger_element(length=step_1, increment=0,
                                               channels=laser_channel)
            rabi_block.append(s1)

            s2 = self._get_trigger_element(length=step_2, increment=0, channels=laser_channel)
            rabi_block.append(s2)

            s3 = self._get_idle_element(length=step_3, increment=0)
            rabi_block.append(s3)

            s4 = self._get_trigger_element(length=step_4, increment=0, channels=mw_channel)
            rabi_block.append(s4)

            s5 = self._get_idle_element(length=step_5 + positive_step * i, increment=0)
            rabi_block.append(s5)

            s6 = self._get_trigger_element(length=step_6, increment=0, channels=mw_channel)
            rabi_block.append(s6)

            s7 = self._get_idle_element(length=step_7 + positive_step * i, increment=0)
            rabi_block.append(s7)

            s8 = self._get_trigger_element(length=step_8, increment=0, channels=mw_channel)
            rabi_block.append(s8)

            s9 = self._get_idle_element(length=step_9, increment=0)
            rabi_block.append(s9)

            s10 = self._get_trigger_element(length=step_10, increment=0, channels=laser_channel)
            rabi_block.append(s10)

            s11 = self._get_idle_element(length=step_11 + negative_step * i, increment=0)
            rabi_block.append(s11)

        created_blocks.append(rabi_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((rabi_block.name, num_of_cycles - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = False
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        # block_ensemble.measurement_information['controlled_variable1'] = ini_mic_delay_array
        # block_ensemble.measurement_information['controlled_variable2'] = microwave_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = num_of_cycles
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # Append ensemble to created_ensembles list
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences
        # *************************************************************************************************
        # *************************************************************************************************

    def generate_pulsedodmr(self, name='pulsedODMR', freq_start=2870.0e6, freq_step=0.2e6,
                            num_of_points=50):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # Create frequency array
        freq_array = freq_start + np.arange(num_of_points) * freq_step

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time,
                                                 increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length,
                                                     increment=0)
        delay_element = self._get_delay_gate_element()

        # Create block and append to created_blocks list
        pulsedodmr_block = PulseBlock(name=name)
        for mw_freq in freq_array:
            mw_element = self._get_mw_element(length=self.rabi_period / 2,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=mw_freq,
                                              phase=0)
            pulsedodmr_block.append(mw_element)
            pulsedodmr_block.append(laser_element)
            pulsedodmr_block.append(delay_element)
            pulsedodmr_block.append(waiting_element)
        created_blocks.append(pulsedodmr_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((pulsedodmr_block.name, 0))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = False
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = freq_array
        block_ensemble.measurement_information['units'] = ('Hz', '')
        block_ensemble.measurement_information['labels'] = ('Frequency', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = num_of_points
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_ramsey(self, name='ramsey', tau_start=1.0e-6, tau_step=1.0e-6, num_of_points=50,
                        alternating=True):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        tau_array = tau_start + np.arange(num_of_points) * tau_step

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time,
                                                 increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length,
                                                     increment=0)
        delay_element = self._get_delay_gate_element()
        pihalf_element = self._get_mw_element(length=self.rabi_period / 4,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)
        # Use a 180 deg phase shiftet pulse as 3pihalf pulse if microwave channel is analog
        if self.microwave_channel.startswith('a'):
            pi3half_element = self._get_mw_element(length=self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=180)
        else:
            pi3half_element = self._get_mw_element(length=3 * self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=0)
        tau_element = self._get_idle_element(length=tau_start, increment=tau_step)

        # Create block and append to created_blocks list
        ramsey_block = PulseBlock(name=name)
        ramsey_block.append(pihalf_element)
        ramsey_block.append(tau_element)
        ramsey_block.append(pihalf_element)
        ramsey_block.append(laser_element)
        ramsey_block.append(delay_element)
        ramsey_block.append(waiting_element)
        if alternating:
            ramsey_block.append(pihalf_element)
            ramsey_block.append(tau_element)
            ramsey_block.append(pi3half_element)
            ramsey_block.append(laser_element)
            ramsey_block.append(delay_element)
            ramsey_block.append(waiting_element)
        created_blocks.append(ramsey_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=True)
        block_ensemble.append((ramsey_block.name, num_of_points - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        number_of_lasers = 2 * num_of_points if alternating else num_of_points
        block_ensemble.measurement_information['alternating'] = alternating
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = tau_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = number_of_lasers
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_ramsey_from_list(self, name='ramsey', tau_list='[1e-6, 2e-6]', alternating = True):
        """

        """

        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        tau_array = [n.strip() for n in tau_list]

        waiting_element = self._get_idle_element(length=self.wait_time,
                                                 increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length,
                                                     increment=0)
        delay_element = self._get_delay_gate_element()
        # get pihalf element
        pihalf_element = self._get_mw_element(length=self.rabi_period / 4,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)

        if alternating:
            if self.microwave_channel.startswith('a'):
                pi3half_element = self._get_mw_element(length=self.rabi_period / 4,
                                                       increment=0,
                                                       amp=self.microwave_amplitude,
                                                       freq=self.microwave_frequency,
                                                       phase=180)
            else:
                pi3half_element = self._get_mw_element(length=3 * self.rabi_period / 4,
                                                       increment=0,
                                                       amp=self.microwave_amplitude,
                                                       freq=self.microwave_frequency,
                                                       phase=0)

        # Create block and append to created_blocks list
        ramsey_block = PulseBlock(name=name)
        for tau in tau_array:
            tau_element = self._get_idle_element(length=tau, increment=0)
            ramsey_block.append(pihalf_element)
            ramsey_block.append(tau_element)
            ramsey_block.append(tau_element)
            ramsey_block.append(pihalf_element)
            ramsey_block.append(laser_element)
            ramsey_block.append(delay_element)
            ramsey_block.append(waiting_element)

            if alternating:
                ramsey_block.append(pihalf_element)
                ramsey_block.append(tau_element)
                ramsey_block.append(pi3half_element)
                ramsey_block.append(laser_element)
                ramsey_block.append(delay_element)
                ramsey_block.append(waiting_element)

        created_blocks.append(ramsey_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=True)
        block_ensemble.append((ramsey_block.name, 0))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        number_of_lasers = 2 * len(tau_array) if alternating else len(tau_array)
        block_ensemble.measurement_information['alternating'] = alternating
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = tau_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = number_of_lasers
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)
        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_hahnecho(self, name='hahn_echo', tau_start=0.0e-6, tau_step=1.0e-6,
                          num_of_points=50, alternating=True):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        tau_array = tau_start + np.arange(num_of_points) * tau_step

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time,
                                                 increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length,
                                                     increment=0)
        delay_element = self._get_delay_gate_element()
        pihalf_element = self._get_mw_element(length=self.rabi_period / 4,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)
        pi_element = self._get_mw_element(length=self.rabi_period / 2,
                                          increment=0,
                                          amp=self.microwave_amplitude,
                                          freq=self.microwave_frequency,
                                          phase=0)
        # Use a 180 deg phase shiftet pulse as 3pihalf pulse if microwave channel is analog
        if self.microwave_channel.startswith('a'):
            pi3half_element = self._get_mw_element(length=self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=180)
        else:
            pi3half_element = self._get_mw_element(length=3 * self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=0)
        tau_element = self._get_idle_element(length=tau_start, increment=tau_step)

        # Create block and append to created_blocks list
        hahn_block = PulseBlock(name=name)
        hahn_block.append(pihalf_element)
        hahn_block.append(tau_element)
        hahn_block.append(pi_element)
        hahn_block.append(tau_element)
        hahn_block.append(pihalf_element)
        hahn_block.append(laser_element)
        hahn_block.append(delay_element)
        hahn_block.append(waiting_element)
        if alternating:
            hahn_block.append(pihalf_element)
            hahn_block.append(tau_element)
            hahn_block.append(pi_element)
            hahn_block.append(tau_element)
            hahn_block.append(pi3half_element)
            hahn_block.append(laser_element)
            hahn_block.append(delay_element)
            hahn_block.append(waiting_element)
        created_blocks.append(hahn_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=True)
        block_ensemble.append((hahn_block.name, num_of_points - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        number_of_lasers = 2 * num_of_points if alternating else num_of_points
        block_ensemble.measurement_information['alternating'] = alternating
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = tau_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = number_of_lasers
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_hahnecho_exp(self, name='hahn_echo', tau_start=1.0e-6, tau_end=1.0e-6,
                                 num_of_points=50, alternating=True):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        if tau_start == 0.0:
            tau_array = np.geomspace(1e-9, tau_end, num_of_points - 1)
            tau_array = np.insert(tau_array, 0, 0.0)
        else:
            tau_array = np.geomspace(tau_start, tau_end, num_of_points)

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time,
                                                 increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length,
                                                     increment=0)
        delay_element = self._get_delay_gate_element()
        pihalf_element = self._get_mw_element(length=self.rabi_period / 4,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)
        pi_element = self._get_mw_element(length=self.rabi_period / 2,
                                          increment=0,
                                          amp=self.microwave_amplitude,
                                          freq=self.microwave_frequency,
                                          phase=0)
        # Use a 180 deg phase shiftet pulse as 3pihalf pulse if microwave channel is analog
        if self.microwave_channel.startswith('a'):
            pi3half_element = self._get_mw_element(length=self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=180)
        else:
            pi3half_element = self._get_mw_element(length=3 * self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=0)

        # Create block and append to created_blocks list
        hahn_block = PulseBlock(name=name)
        for tau in tau_array:
            tau_element = self._get_idle_element(length=tau, increment=0.0)
            hahn_block.append(pihalf_element)
            hahn_block.append(tau_element)
            hahn_block.append(pi_element)
            hahn_block.append(tau_element)
            hahn_block.append(pihalf_element)
            hahn_block.append(laser_element)
            hahn_block.append(delay_element)
            hahn_block.append(waiting_element)
            if alternating:
                hahn_block.append(pihalf_element)
                hahn_block.append(tau_element)
                hahn_block.append(pi_element)
                hahn_block.append(tau_element)
                hahn_block.append(pi3half_element)
                hahn_block.append(laser_element)
                hahn_block.append(delay_element)
                hahn_block.append(waiting_element)
        created_blocks.append(hahn_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((hahn_block.name, 0))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        number_of_lasers = 2 * num_of_points if alternating else num_of_points
        block_ensemble.measurement_information['alternating'] = alternating
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = tau_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = number_of_lasers
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)
        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_t1(self, name='T1', tau_start=1.0e-6, tau_step=1.0e-6,
                    num_of_points=50, alternating = False):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        tau_array = tau_start + np.arange(num_of_points) * tau_step

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time,
                                                 increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length,
                                                     increment=0)
        delay_element = self._get_delay_gate_element()
        if alternating: # get pi element
            pi_element = self._get_mw_element(length=self.rabi_period / 2,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)

        tau_element = self._get_idle_element(length=tau_start, increment=tau_step)
        t1_block = PulseBlock(name=name)
        t1_block.append(tau_element)
        t1_block.append(laser_element)
        t1_block.append(delay_element)
        t1_block.append(waiting_element)
        if alternating:
            t1_block.append(pi_element)
            t1_block.append(tau_element)
            t1_block.append(laser_element)
            t1_block.append(delay_element)
            t1_block.append(waiting_element)
        created_blocks.append(t1_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((t1_block.name, num_of_points - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        number_of_lasers = 2 * num_of_points if alternating else num_of_points
        block_ensemble.measurement_information['alternating'] = alternating
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = tau_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = number_of_lasers
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)
        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_t1_exponential(self, name='T1_exp', tau_start=1.0e-6, tau_end=1.0e-6,
                    num_of_points=50, alternating=False):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        if tau_start == 0.0:
            tau_array = np.geomspace(1e-9, tau_end, num_of_points - 1)
            tau_array = np.insert(tau_array, 0, 0.0)
        else:
            tau_array = np.geomspace(tau_start, tau_end, num_of_points)

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time,
                                                 increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length,
                                                     increment=0)
        delay_element = self._get_delay_gate_element()
        if alternating:  # get pi element
            pi_element = self._get_mw_element(length=self.rabi_period / 2,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)
        t1_block = PulseBlock(name=name)
        for tau in tau_array:
            tau_element = self._get_idle_element(length=tau, increment=0.0)
            t1_block.append(tau_element)
            t1_block.append(laser_element)
            t1_block.append(delay_element)
            t1_block.append(waiting_element)
            if alternating:
                t1_block.append(pi_element)
                t1_block.append(tau_element)
                t1_block.append(laser_element)
                t1_block.append(delay_element)
                t1_block.append(waiting_element)
        created_blocks.append(t1_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=False)
        block_ensemble.append((t1_block.name, 0))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        number_of_lasers = 2 * num_of_points if alternating else num_of_points
        block_ensemble.measurement_information['alternating'] = alternating
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = tau_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = number_of_lasers
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)
        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_HHamp(self, name='hh_amp', spinlock_length=20e-6, amp_start=0.05, amp_step=0.01,
                       num_of_points=50):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get amplitude array for measurement ticks
        amp_array = amp_start + np.arange(num_of_points) * amp_step

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time, increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length, increment=0)
        delay_element = self._get_delay_gate_element()
        pihalf_element = self._get_mw_element(length=self.rabi_period / 4,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)
        # Use a 180 deg phase shiftet pulse as 3pihalf pulse if microwave channel is analog
        if self.microwave_channel.startswith('a'):
            pi3half_element = self._get_mw_element(length=self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=180)
        else:
            pi3half_element = self._get_mw_element(length=3 * self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=0)

        # Create block and append to created_blocks list
        hhamp_block = PulseBlock(name=name)
        for sl_amp in amp_array:
            sl_element = self._get_mw_element(length=spinlock_length,
                                              increment=0,
                                              amp=sl_amp,
                                              freq=self.microwave_frequency,
                                              phase=90)
            hhamp_block.append(pihalf_element)
            hhamp_block.append(sl_element)
            hhamp_block.append(pihalf_element)
            hhamp_block.append(laser_element)
            hhamp_block.append(delay_element)
            hhamp_block.append(waiting_element)

            hhamp_block.append(pi3half_element)
            hhamp_block.append(sl_element)
            hhamp_block.append(pihalf_element)
            hhamp_block.append(laser_element)
            hhamp_block.append(delay_element)
            hhamp_block.append(waiting_element)
        created_blocks.append(hhamp_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=True)
        block_ensemble.append((hhamp_block.name, 0))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = True
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = amp_array
        block_ensemble.measurement_information['units'] = ('V', '')
        block_ensemble.measurement_information['labels'] = ('MW amplitude', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = 2 * num_of_points
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_HHtau(self, name='hh_tau', spinlock_amp=0.1, tau_start=1e-6, tau_step=1e-6,
                       num_of_points=50):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        tau_array = tau_start + np.arange(num_of_points) * tau_step

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time, increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length, increment=0)
        delay_element = self._get_delay_gate_element()
        pihalf_element = self._get_mw_element(length=self.rabi_period / 4,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)
        # Use a 180 deg phase shiftet pulse as 3pihalf pulse if microwave channel is analog
        if self.microwave_channel.startswith('a'):
            pi3half_element = self._get_mw_element(length=self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=180)
        else:
            pi3half_element = self._get_mw_element(length=3 * self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=0)
        sl_element = self._get_mw_element(length=tau_start,
                                          increment=tau_step,
                                          amp=spinlock_amp,
                                          freq=self.microwave_frequency,
                                          phase=90)

        # Create block and append to created_blocks list
        hhtau_block = PulseBlock(name=name)
        hhtau_block.append(pihalf_element)
        hhtau_block.append(sl_element)
        hhtau_block.append(pihalf_element)
        hhtau_block.append(laser_element)
        hhtau_block.append(delay_element)
        hhtau_block.append(waiting_element)

        hhtau_block.append(pi3half_element)
        hhtau_block.append(sl_element)
        hhtau_block.append(pihalf_element)
        hhtau_block.append(laser_element)
        hhtau_block.append(delay_element)
        hhtau_block.append(waiting_element)
        created_blocks.append(hhtau_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=True)
        block_ensemble.append((hhtau_block.name, num_of_points - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = True
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = tau_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Spinlock time', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = 2 * num_of_points
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_HHpol(self, name='hh_pol', spinlock_length=20.0e-6, spinlock_amp=0.1,
                       polarization_steps=50):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get steps array for measurement ticks
        steps_array = np.arange(2 * polarization_steps)

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time, increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length, increment=0)
        delay_element = self._get_delay_gate_element()
        pihalf_element = self._get_mw_element(length=self.rabi_period / 4,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)
        # Use a 180 deg phase shiftet pulse as 3pihalf pulse if microwave channel is analog
        if self.microwave_channel.startswith('a'):
            pi3half_element = self._get_mw_element(length=self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=180)
        else:
            pi3half_element = self._get_mw_element(length=3 * self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=0)
        sl_element = self._get_mw_element(length=spinlock_length,
                                          increment=0,
                                          amp=spinlock_amp,
                                          freq=self.microwave_frequency,
                                          phase=90)

        # Create block for "up"-polarization and append to created_blocks list
        up_block = PulseBlock(name=name + '_up')
        up_block.append(pihalf_element)
        up_block.append(sl_element)
        up_block.append(pihalf_element)
        up_block.append(laser_element)
        up_block.append(delay_element)
        up_block.append(waiting_element)
        created_blocks.append(up_block)

        # Create block for "down"-polarization and append to created_blocks list
        down_block = PulseBlock(name=name + '_down')
        down_block.append(pi3half_element)
        down_block.append(sl_element)
        down_block.append(pi3half_element)
        down_block.append(laser_element)
        down_block.append(delay_element)
        down_block.append(waiting_element)
        created_blocks.append(down_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=True)
        block_ensemble.append((up_block.name, polarization_steps - 1))
        block_ensemble.append((down_block.name, polarization_steps - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        block_ensemble.measurement_information['alternating'] = False
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = steps_array
        block_ensemble.measurement_information['units'] = ('#', '')
        block_ensemble.measurement_information['labels'] = ('Polarization Steps', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = 2 * polarization_steps
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_xy8_tau(self, name='xy8_tau', tau_start=0.5e-6, tau_step=0.01e-6, num_of_points=50,
                         xy8_order=4, alternating=True):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get tau array for measurement ticks
        tau_array = tau_start + np.arange(num_of_points) * tau_step
        # calculate "real" start length of tau due to finite pi-pulse length
        real_start_tau = max(0, tau_start - self.rabi_period / 2)

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time, increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length, increment=0)
        delay_element = self._get_delay_gate_element()
        pihalf_element = self._get_mw_element(length=self.rabi_period / 4,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)
        # Use a 180 deg phase shiftet pulse as 3pihalf pulse if microwave channel is analog
        if self.microwave_channel.startswith('a'):
            pi3half_element = self._get_mw_element(length=self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=180)
        else:
            pi3half_element = self._get_mw_element(length=3 * self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=0)
        pix_element = self._get_mw_element(length=self.rabi_period / 2,
                                           increment=0,
                                           amp=self.microwave_amplitude,
                                           freq=self.microwave_frequency,
                                           phase=0)
        piy_element = self._get_mw_element(length=self.rabi_period / 2,
                                           increment=0,
                                           amp=self.microwave_amplitude,
                                           freq=self.microwave_frequency,
                                           phase=90)
        tauhalf_element = self._get_idle_element(length=real_start_tau / 2, increment=tau_step / 2)
        tau_element = self._get_idle_element(length=real_start_tau, increment=tau_step)

        # Create block and append to created_blocks list
        xy8_block = PulseBlock(name=name)
        xy8_block.append(pihalf_element)
        xy8_block.append(tauhalf_element)
        for n in range(xy8_order):
            xy8_block.append(pix_element)
            xy8_block.append(tau_element)
            xy8_block.append(piy_element)
            xy8_block.append(tau_element)
            xy8_block.append(pix_element)
            xy8_block.append(tau_element)
            xy8_block.append(piy_element)
            xy8_block.append(tau_element)
            xy8_block.append(piy_element)
            xy8_block.append(tau_element)
            xy8_block.append(pix_element)
            xy8_block.append(tau_element)
            xy8_block.append(piy_element)
            xy8_block.append(tau_element)
            xy8_block.append(pix_element)
            if n != xy8_order - 1:
                xy8_block.append(tau_element)
        xy8_block.append(tauhalf_element)
        xy8_block.append(pihalf_element)
        xy8_block.append(laser_element)
        xy8_block.append(delay_element)
        xy8_block.append(waiting_element)
        if alternating:
            xy8_block.append(pihalf_element)
            xy8_block.append(tauhalf_element)
            for n in range(xy8_order):
                xy8_block.append(pix_element)
                xy8_block.append(tau_element)
                xy8_block.append(piy_element)
                xy8_block.append(tau_element)
                xy8_block.append(pix_element)
                xy8_block.append(tau_element)
                xy8_block.append(piy_element)
                xy8_block.append(tau_element)
                xy8_block.append(piy_element)
                xy8_block.append(tau_element)
                xy8_block.append(pix_element)
                xy8_block.append(tau_element)
                xy8_block.append(piy_element)
                xy8_block.append(tau_element)
                xy8_block.append(pix_element)
                if n != xy8_order - 1:
                    xy8_block.append(tau_element)
            xy8_block.append(tauhalf_element)
            xy8_block.append(pi3half_element)
            xy8_block.append(laser_element)
            xy8_block.append(delay_element)
            xy8_block.append(waiting_element)
        created_blocks.append(xy8_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=True)
        block_ensemble.append((xy8_block.name, num_of_points - 1))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        number_of_lasers = num_of_points * 2 if alternating else num_of_points
        block_ensemble.measurement_information['alternating'] = alternating
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = tau_array
        block_ensemble.measurement_information['units'] = ('s', '')
        block_ensemble.measurement_information['labels'] = ('Tau', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = number_of_lasers
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    def generate_xy8_freq(self, name='xy8_freq', freq_start=0.1e6, freq_step=0.01e6,
                          num_of_points=50, xy8_order=4, alternating=True):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # get frequency array for measurement ticks
        freq_array = freq_start + np.arange(num_of_points) * freq_step
        # get tau array from freq array
        tau_array = 1 / (2 * freq_array)
        # calculate "real" tau array (finite pi-pulse length)
        real_tau_array = tau_array - self.rabi_period / 2
        np.clip(real_tau_array, 0, None, real_tau_array)
        # Convert back to frequency in order to account for clipped values
        freq_array = 1 / (2 * (real_tau_array + self.rabi_period / 2))

        # create the elements
        waiting_element = self._get_idle_element(length=self.wait_time, increment=0)
        laser_element = self._get_laser_gate_element(length=self.laser_length, increment=0)
        delay_element = self._get_delay_gate_element()
        pihalf_element = self._get_mw_element(length=self.rabi_period / 4,
                                              increment=0,
                                              amp=self.microwave_amplitude,
                                              freq=self.microwave_frequency,
                                              phase=0)
        # Use a 180 deg phase shiftet pulse as 3pihalf pulse if microwave channel is analog
        if self.microwave_channel.startswith('a'):
            pi3half_element = self._get_mw_element(length=self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=180)
        else:
            pi3half_element = self._get_mw_element(length=3 * self.rabi_period / 4,
                                                   increment=0,
                                                   amp=self.microwave_amplitude,
                                                   freq=self.microwave_frequency,
                                                   phase=0)
        pix_element = self._get_mw_element(length=self.rabi_period / 2,
                                           increment=0,
                                           amp=self.microwave_amplitude,
                                           freq=self.microwave_frequency,
                                           phase=0)
        piy_element = self._get_mw_element(length=self.rabi_period / 2,
                                           increment=0,
                                           amp=self.microwave_amplitude,
                                           freq=self.microwave_frequency,
                                           phase=90)

        # Create block and append to created_blocks list
        xy8_block = PulseBlock(name=name)
        for ii, tau in enumerate(real_tau_array):
            tauhalf_element = self._get_idle_element(length=tau / 2, increment=0)
            tau_element = self._get_idle_element(length=tau, increment=0)
            xy8_block.append(pihalf_element)
            xy8_block.append(tauhalf_element)
            for n in range(xy8_order):
                xy8_block.append(pix_element)
                xy8_block.append(tau_element)
                xy8_block.append(piy_element)
                xy8_block.append(tau_element)
                xy8_block.append(pix_element)
                xy8_block.append(tau_element)
                xy8_block.append(piy_element)
                xy8_block.append(tau_element)
                xy8_block.append(piy_element)
                xy8_block.append(tau_element)
                xy8_block.append(pix_element)
                xy8_block.append(tau_element)
                xy8_block.append(piy_element)
                xy8_block.append(tau_element)
                xy8_block.append(pix_element)
                if n != xy8_order - 1:
                    xy8_block.append(tau_element)
            xy8_block.append(tauhalf_element)
            xy8_block.append(pihalf_element)
            xy8_block.append(laser_element)
            xy8_block.append(delay_element)
            xy8_block.append(waiting_element)
            if alternating:
                xy8_block.append(pihalf_element)
                xy8_block.append(tauhalf_element)
                for n in range(xy8_order):
                    xy8_block.append(pix_element)
                    xy8_block.append(tau_element)
                    xy8_block.append(piy_element)
                    xy8_block.append(tau_element)
                    xy8_block.append(pix_element)
                    xy8_block.append(tau_element)
                    xy8_block.append(piy_element)
                    xy8_block.append(tau_element)
                    xy8_block.append(piy_element)
                    xy8_block.append(tau_element)
                    xy8_block.append(pix_element)
                    xy8_block.append(tau_element)
                    xy8_block.append(piy_element)
                    xy8_block.append(tau_element)
                    xy8_block.append(pix_element)
                    if n != xy8_order - 1:
                        xy8_block.append(tau_element)
                xy8_block.append(tauhalf_element)
                xy8_block.append(pi3half_element)
                xy8_block.append(laser_element)
                xy8_block.append(delay_element)
                xy8_block.append(waiting_element)
        created_blocks.append(xy8_block)

        # Create block ensemble
        block_ensemble = PulseBlockEnsemble(name=name, rotating_frame=True)
        block_ensemble.append((xy8_block.name, 0))

        # Create and append sync trigger block if needed
        self._add_trigger(created_blocks=created_blocks, block_ensemble=block_ensemble)

        # add metadata to invoke settings later on
        number_of_lasers = num_of_points * 2 if alternating else num_of_points
        block_ensemble.measurement_information['alternating'] = alternating
        block_ensemble.measurement_information['laser_ignore_list'] = list()
        block_ensemble.measurement_information['controlled_variable'] = freq_array
        block_ensemble.measurement_information['units'] = ('Hz', '')
        block_ensemble.measurement_information['labels'] = ('Frequency', 'Signal')
        block_ensemble.measurement_information['number_of_lasers'] = number_of_lasers
        block_ensemble.measurement_information['counting_length'] = self._get_ensemble_count_length(
            ensemble=block_ensemble, created_blocks=created_blocks)

        # append ensemble to created ensembles
        created_ensembles.append(block_ensemble)
        return created_blocks, created_ensembles, created_sequences

    ################################################################################################
    #                             Generation methods for sequences                                 #
    ################################################################################################
    def generate_t1_sequencing(self, name='t1_seq', tau_start=1.0e-6, tau_max=1.0e-3,
                               num_of_points=10):
        """

        """
        created_blocks = list()
        created_ensembles = list()
        created_sequences = list()

        # Get logarithmically spaced steps in multiples of tau_start.
        # Note that the number of points and the position of the last point can change here.
        k_array = np.unique(
            np.rint(np.logspace(0., np.log10(tau_max / tau_start), num_of_points)).astype(int))
        # get tau array for measurement ticks
        tau_array = k_array * tau_start

        # Create the readout PulseBlockEnsemble
        # Get necessary PulseBlockElements
        laser_element = self._get_laser_gate_element(length=self.laser_length,  increment=0)
        delay_element = self._get_delay_gate_element()
        # Create PulseBlock and append PulseBlockElements
        readout_block = PulseBlock(name='{0}_readout'.format(name))
        readout_block.append(laser_element)
        readout_block.append(delay_element)
        created_blocks.append(readout_block)
        # Create PulseBlockEnsemble and append block to it
        readout_ensemble = PulseBlockEnsemble(name='{0}_readout'.format(name), rotating_frame=False)
        readout_ensemble.append((readout_block.name, 0))
        created_ensembles.append(readout_ensemble)

        if self.sync_channel:
            # Create the last readout PulseBlockEnsemble including a sync trigger
            # Get necessary PulseBlockElements
            sync_element = self._get_sync_element()
            # Create PulseBlock and append PulseBlockElements
            sync_readout_block = PulseBlock(name='{0}_readout_sync'.format(name))
            sync_readout_block.append(laser_element)
            sync_readout_block.append(delay_element)
            sync_readout_block.append(sync_element)
            created_blocks.append(sync_readout_block)
            # Create PulseBlockEnsemble and append block to it
            sync_readout_ensemble = PulseBlockEnsemble(name='{0}_readout_sync'.format(name),
                                                       rotating_frame=False)
            sync_readout_ensemble.append((sync_readout_block.name, 0))
            created_ensembles.append(sync_readout_ensemble)

        # Create the tau/waiting PulseBlockEnsemble
        # Get tau PulseBlockElement
        tau_element = self._get_idle_element(length=tau_start, increment=0)
        # Create PulseBlock and append PulseBlockElements
        tau_block = PulseBlock(name='{0}_tau'.format(name))
        tau_block.append(tau_element)
        created_blocks.append(tau_block)
        # Create PulseBlockEnsemble and append block to it
        tau_ensemble = PulseBlockEnsemble(name='{0}_tau'.format(name), rotating_frame=False)
        tau_ensemble.append((tau_block.name, 0))
        created_ensembles.append(tau_ensemble)

        # Create the PulseSequence and append the PulseBlockEnsemble names as sequence steps
        # together with the necessary parameters.
        t1_sequence = PulseSequence(name=name, rotating_frame=False)
        count_length = 0.0
        for k in k_array:
            t1_sequence.append(tau_ensemble.name)
            t1_sequence[-1].repetitions = int(k) - 1
            count_length += k * self._get_ensemble_count_length(ensemble=tau_ensemble,
                                                                created_blocks=created_blocks)

            if self.sync_channel and k == k_array[-1]:
                t1_sequence.append(sync_readout_ensemble.name)
            else:
                t1_sequence.append(readout_ensemble.name)
            count_length += self._get_ensemble_count_length(ensemble=readout_ensemble,
                                                            created_blocks=created_blocks)
        # Make the sequence loop infinitely by setting the go_to parameter of the last sequence
        # step to the first step.
        t1_sequence[-1].go_to = 1

        # Trigger the calculation of parameters in the PulseSequence instance
        t1_sequence.refresh_parameters()

        # add metadata to invoke settings later on
        t1_sequence.measurement_information['alternating'] = False
        t1_sequence.measurement_information['laser_ignore_list'] = list()
        t1_sequence.measurement_information['controlled_variable'] = tau_array
        t1_sequence.measurement_information['units'] = ('s', '')
        t1_sequence.measurement_information['number_of_lasers'] = len(tau_array)
        t1_sequence.measurement_information['counting_length'] = count_length

        # Append PulseSequence to created_sequences list
        created_sequences.append(t1_sequence)
        return created_blocks, created_ensembles, created_sequences
