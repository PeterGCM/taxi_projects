#!/usr/bin/env bash

python -c "from b4_individualAnalysis import locIn_Reg; locIn_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_D_Reg; locIn_F_D_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_H_Reg; locIn_F_H_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_M_Reg; locIn_F_M_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_DH_Reg; locIn_F_DH_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_DM_Reg; locIn_F_DM_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_HM_Reg; locIn_F_HM_Reg()" &
python -c "from b4_individualAnalysis import locIn_F_DHM_Reg; locIn_F_DHM_Reg()" &