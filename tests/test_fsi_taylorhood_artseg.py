#!/usr/bin/env python3

"""
FSI of arterial segment: Q2-Q1 Taylor-Hood for both fluid and incompressible solid
"""

import ambit_fe

import sys, traceback
import numpy as np
from pathlib import Path
import pytest


@pytest.mark.fsi
@pytest.mark.fluid_solid
def test_main():

    basepath = str(Path(__file__).parent.absolute())

    IO_PARAMS            = {'problem_type'          : 'fsi',
                            'write_results_every'   : 1,
                            'indicate_results_by'   : 'step',
                            'output_path'           : basepath+'/tmp/',
                            'mesh_domain'           : basepath+'/input/artseg-fsi-hex-quad_domain.xdmf',
                            'mesh_boundary'         : basepath+'/input/artseg-fsi-hex-quad_boundary.xdmf',
                            'results_to_write'      : [['displacement','velocity'], [['fluiddisplacement','velocity','pressure'],['aledisplacement','alevelocity']]],
                            'domain_ids_solid'      : [1],
                            'domain_ids_fluid'      : [2],
                            'surface_ids_interface' : [1],
                            'simname'               : 'fsi_taylorhood_artseg'}

    SOLVER_PARAMS        = {'solve_type'            : 'direct',
                            'direct_solver'         : 'mumps',
                            'tol_res'               : [1e-8,1e-8,1e-8,1e-8,1e-8,1e-6],
                            'tol_inc'               : [1e-0,1e-0,1e-0,1e-0,1e-0,1e-0]}

    TIME_PARAMS_SOLID    = {'maxtime'               : 0.1,
                            'dt'                    : 0.02,
                            'timint'                : 'ost',
                            'theta_ost'             : 1.0}

    TIME_PARAMS_FLUID    = {'maxtime'               : 0.1,
                            'dt'                    : 0.02,
                            'timint'                : 'ost',
                            'theta_ost'             : 1.0}

    FEM_PARAMS_SOLID     = {'order_disp'            : 2,
                            'order_pres'            : 1,
                            'quad_degree'           : 5,
                            'incompressibility'     : 'full'}

    FEM_PARAMS_FLUID     = {'order_vel'             : 2,
                            'order_pres'            : 1,
                            'quad_degree'           : 5}

    FEM_PARAMS_ALE       = {'order_disp'            : 2,
                            'quad_degree'           : 5}

    COUPLING_PARAMS      = {'coupling_fluid_ale'    : [{'surface_ids' : [1], 'type' : 'strong_dirichlet'}],
                            'fsi_governing_type'    : 'fluid_governed'} # solid_governed, fluid_governed

    MATERIALS_SOLID      = {'MAT1' : {'neohooke_dev'      : {'mu' : 100.},
                                      'inertia'           : {'rho0' : 1.0e-6}}}

    MATERIALS_FLUID      = {'MAT1' : {'newtonian' : {'mu' : 4.0e-6},
                                      'inertia' : {'rho' : 1.025e-6}}}

    MATERIALS_ALE        = {'MAT1' : {'linelast' : {'Emod' : 2.0, 'nu' : 0.1}}}


    # define your load curves here (syntax: tcX refers to curve X, to be used in BC_DICT key 'curve' : [X,0,0], or 'curve' : X)
    class time_curves:

        def tc1(self, t):
            t_ramp = 2.0
            p0 = 0.0
            pinfl = 0.1
            return (0.5*(-(pinfl-p0))*(1.-np.cos(np.pi*t/t_ramp)) + (-p0)) * (t<t_ramp) + (-pinfl)*(t>=t_ramp)


    BC_DICT_SOLID        = { 'dirichlet' : [{'id' : [2,4], 'dir' : 'z', 'val' : 0.},
                                            {'id' : [6], 'dir' : 'y', 'val' : 0.},
                                            {'id' : [8], 'dir' : 'x', 'val' : 0.}]}

    BC_DICT_FLUID        = { 'neumann' :   [{'id' : [3,5], 'dir' : 'normal_cur', 'curve' : 1}],
                             'dirichlet' : [{'id' : [7], 'dir' : 'y', 'val' : 0.},
                                            {'id' : [9], 'dir' : 'x', 'val' : 0.}] }

    BC_DICT_ALE          = { 'dirichlet' : [{'id' : [3,5], 'dir' : 'z', 'val' : 0.},
                                            {'id' : [7], 'dir' : 'y', 'val' : 0.},
                                            {'id' : [9], 'dir' : 'x', 'val' : 0.}] }


    # problem setup
    problem = ambit_fe.ambit_main.Ambit(IO_PARAMS, [TIME_PARAMS_SOLID, TIME_PARAMS_FLUID], SOLVER_PARAMS, [FEM_PARAMS_SOLID, FEM_PARAMS_FLUID, FEM_PARAMS_ALE], [MATERIALS_SOLID, MATERIALS_FLUID, MATERIALS_ALE], [BC_DICT_SOLID, BC_DICT_FLUID, BC_DICT_ALE], time_curves=time_curves(), coupling_params=COUPLING_PARAMS)

    # problem solve
    problem.solve_problem()


    # --- results check
    tol = 1.0e-6

    check_node = []
    check_node.append(np.array([7.07107, 7.07107, 2.5]))

    u_corr, v_corr = np.zeros(3*len(check_node)), np.zeros(3*len(check_node))

    # correct results
    u_corr[0] = 1.2538881876233117E-04 # x
    u_corr[1] = 1.2538882125343086E-04 # y
    u_corr[2] = 0.0 # z

    v_corr[0] = 2.2544983563815716E-03 # x
    v_corr[1] = 2.2544983916726047E-03 # y
    v_corr[2] = 0.0 # z

    check1 = ambit_fe.resultcheck.results_check_node(problem.mp.pbs.u, check_node, u_corr, problem.mp.pbs.V_u, problem.mp.comm, tol=tol, nm='u', readtol=1e-4)
    check2 = ambit_fe.resultcheck.results_check_node(problem.mp.pbf.v, check_node, v_corr, problem.mp.pbf.V_v, problem.mp.comm, tol=tol, nm='v', readtol=1e-4)

    success = ambit_fe.resultcheck.success_check([check1,check2], problem.mp.comm)

    if not success:
        raise RuntimeError("Test failed!")



if __name__ == "__main__":

    test_main()
