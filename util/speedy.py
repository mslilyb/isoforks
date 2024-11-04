import glob
import subprocess
import statistics
import sys
import time

if len(sys.argv) == 1: sys.exit('provide a limit')
verbose = False
if len(sys.argv) == 3:
        verbose = True

limit = int(sys.argv[1])

params = '--apwm models/acc.pwm --dpwm models/don.pwm --emm models/exon.mm --imm models/intron.mm --elen models/exon.len --ilen models/intron.len'
params2 = '--apwm models/acc.pwm --dpwm models/don.pwm --emm models/exon.mm --imm models/intron.mm --elen models/exon.len --ilen models/intron.len'

t0 = time.time()
ffs = sorted(glob.glob(f'apc/*.fa'))
gffs = sorted(glob.glob(f'apc/*.gff3'))
ratios = []
for n, (ff, gff) in enumerate(zip(ffs, gffs)):
        t0 = time.time()
        subprocess.run(f'isoformer {ff} {params} > /dev/null', shell=True)
        t1 = time.time()
        subprocess.run(f'isoformer {ff} --introns {gff} {params} > /dev/null', shell=True)
        t2 = time.time()
        e1 = t1 - t0
        e2 = t2 - t1
        if verbose:
                print(ff, e1, e2, e2/e1)
        ratios.append(e2/e1)
        n += 1
        if n == limit: break

print(statistics.mean(ratios), '+/-', statistics.stdev(ratios))
