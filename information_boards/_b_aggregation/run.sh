#!/usr/bin/env bash

python -c "from b4_individualAnalysis import locIn_Reg; locIn_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_W_Reg; locIn_F_W_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_H_Reg; locIn_F_H_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_M_Reg; locIn_F_M_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_WH_Reg; locIn_F_WH_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_WM_Reg; locIn_F_WM_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_HM_Reg; locIn_F_HM_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_WHM_Reg; locIn_F_WHM_Reg()" &