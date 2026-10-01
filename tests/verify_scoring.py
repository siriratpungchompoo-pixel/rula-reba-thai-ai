from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scoring import score_rula, score_reba

# ตัวอย่าง RULA จากแบบประเมิน: A=4, B=2 -> Final=3
r = score_rula({
    'upper_arm_angle':30, 'upper_arm_direction':'flex',
    'lower_arm_angle':110,
    'wrist_angle':20, 'wrist_twist_end':True,
    'static_a':True, 'force_a':0,
    'neck_angle':15, 'neck_direction':'flex',
    'trunk_angle':10, 'legs_supported':True,
    'static_b':False, 'force_b':0,
})
assert r['posture_a'] == 3
assert r['final_a'] == 4
assert r['posture_b'] == 2
assert r['final_b'] == 2
assert r['final'] == 3

# smoke test REBA
q = score_reba({
    'neck_angle':10, 'neck_direction':'flex',
    'trunk_angle':30, 'trunk_direction':'flex',
    'knee_angle':35, 'legs_supported':True,
    'upper_arm_angle':50, 'upper_arm_direction':'flex',
    'lower_arm_angle':90, 'wrist_angle':10,
    'load':0, 'coupling':0,
})
assert 1 <= q['final'] <= 15
print('ตรวจสอบ scoring ผ่าน')
