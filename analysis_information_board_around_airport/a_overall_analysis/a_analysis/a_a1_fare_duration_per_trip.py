from __future__ import division
#
import os, sys  
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn
from supports._setting import DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS
from supports._setting import DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP
from supports._setting import CENT, SEC60
from supports.charts import simple_barchart
#
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#
def run():
    ap_analysis()
    ns_analysis()

def ap_analysis():
    trip_df = pd.read_csv(ap_tm_num_dur_fare_fn)
    gb = trip_df.groupby('ap-trip-mode')
    #
    # calculate statistics
    #
    ap_in_num = gb.sum()['num-tm'][DInAP_PInAP] + gb.sum()['num-tm'][DOutAP_PInAP]
    ap_in_fare = (gb.sum()['total-fare'][DInAP_PInAP] + gb.sum()['total-fare'][DOutAP_PInAP]) / CENT
    ap_in_dur = (gb.sum()['total-dur'][DInAP_PInAP] + gb.sum()['total-dur'][DOutAP_PInAP]) / SEC60
    #
    ap_in_fare_per_trip = ap_in_fare / ap_in_num
    ap_in_dur_per_trip = ap_in_dur / ap_in_num
    #
    ap_out_num = gb.sum()['num-tm'][DInAP_POutAP] + gb.sum()['num-tm'][DOutAP_POutAP]
    ap_out_fare = (gb.sum()['total-fare'][DInAP_POutAP] + gb.sum()['total-fare'][DOutAP_POutAP]) / CENT
    ap_out_dur = (gb.sum()['total-dur'][DInAP_POutAP] + gb.sum()['total-dur'][DOutAP_POutAP]) / SEC60
    #
    ap_out_fare_per_trip = ap_out_fare / ap_out_num
    ap_out_dur_per_trip = ap_out_dur / ap_out_num
    #
    # charts
    #
    _data = [ap_in_fare_per_trip, ap_out_fare_per_trip]
    simple_barchart(['Airport', 'Other areas'], 'S$', _data, 'fare_per_trip_ap')
    #
    _data = [ap_in_dur_per_trip, ap_out_dur_per_trip]
    simple_barchart(['Airport', 'Other areas'], 'Minute', _data, 'dur_per_trip_ap')

def ns_analysis():
    trip_df = pd.read_csv(ns_tm_num_dur_fare_fn)
    gb = trip_df.groupby('ns-trip-mode')
    #
    # calculate statistics
    #
    ns_in_num = gb.sum()['num-tm'][DInNS_PInNS] + gb.sum()['num-tm'][DOutNS_PInNS]
    ns_in_fare = (gb.sum()['total-fare'][DInNS_PInNS] + gb.sum()['total-fare'][DOutNS_PInNS]) / CENT
    ns_in_dur = (gb.sum()['total-dur'][DInNS_PInNS] + gb.sum()['total-dur'][DOutNS_PInNS]) / SEC60
    #
    ns_in_fare_per_trip = ns_in_fare / ns_in_num
    ns_in_dur_per_trip = ns_in_dur / ns_in_num
    #
    ns_out_num = gb.sum()['num-tm'][DInNS_POutNS] + gb.sum()['num-tm'][DOutNS_POutNS]
    ns_out_fare = (gb.sum()['total-fare'][DInNS_POutNS] + gb.sum()['total-fare'][DOutNS_POutNS]) / CENT
    ns_out_dur = (gb.sum()['total-dur'][DInNS_POutNS] + gb.sum()['total-dur'][DOutNS_POutNS]) / SEC60
    #
    ns_out_fare_per_trip = ns_out_fare / ns_out_num
    ns_out_dur_per_trip = ns_out_dur / ns_out_num
    #
    # charts
    #
    _data = [ns_in_fare_per_trip, ns_out_fare_per_trip]
    simple_barchart(['Night safari', 'Other areas'], 'S$', _data, 'fare_per_trip_ns')
    #
    _data = [ns_in_dur_per_trip, ns_out_dur_per_trip]
    simple_barchart(['Night safari', 'Other areas'], 'Minute', _data, 'dur_per_trip_ns')

if __name__ == '__main__':
    run()
