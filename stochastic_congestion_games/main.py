import __init__


def run(problem, algorithm):
    algorithm(*problem())



if __name__ == '__main__':
    from problems import p1
    from MDPs.FP_SAP import run as run_FP_SAP
    run(p1, run_FP_SAP)

