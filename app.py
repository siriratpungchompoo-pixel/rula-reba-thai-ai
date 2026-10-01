from __future__ import annotations
import io, math, os, json
from datetime import date
import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title='RULA / REBA ภาษาไทย + AI', page_icon='🧍', layout='wide')
st.title('RULA / REBA ภาษาไทย พร้อม AI ช่วยประเมิน')
st.caption('อัปโหลดภาพ → AI ช่วยวัดมุม → ผู้ประเมินยืนยันตัวแปร → คะแนนก่อน/หลัง → PDF')
st.warning('AI เป็นเครื่องมือช่วยคัดกรองจากภาพ 2 มิติ ไม่ควรใช้แทนการประเมินหน้างานจริง')

def clamp(x,a,b): return max(a,min(b,x))
RULA_C=[None,[None,1,2,3,3,4,5,5],[None,2,2,3,4,4,5,5],[None,3,3,3,4,4,5,6],[None,3,3,3,4,5,6,6],[None,4,4,4,5,6,7,7],[None,4,4,5,6,6,7,7],[None,5,5,6,6,7,7,7],[None,5,5,6,7,7,7,7]]
RULA_A={
1:{1:[[1,2],[2,2],[2,3],[3,3]],2:[[2,2],[2,2],[3,3],[3,3]],3:[[2,3],[2,3],[3,3],[4,4]]},
2:{1:[[2,2],[2,3],[3,3],[4,4]],2:[[2,2],[2,3],[3,3],[4,4]],3:[[2,3],[3,3],[3,4],[4,5]]},
3:{1:[[2,3],[3,3],[4,4],[5,5]],2:[[2,3],[3,3],[4,4],[5,5]],3:[[2,3],[3,4],[4,4],[5,5]]},
4:{1:[[3,4],[4,4],[4,4],[5,5]],2:[[3,4],[4,4],[4,4],[5,5]],3:[[3,4],[4,5],[5,5],[6,6]]},
5:{1:[[5,5],[5,5],[5,6],[6,7]],2:[[5,6],[6,6],[6,7],[7,7]],3:[[6,6],[6,7],[7,7],[7,8]]},
6:{1:[[7,7],[7,7],[7,8],[8,9]],2:[[7,8],[8,8],[8,9],[9,9]],3:[[9,9],[9,9],[9,9],[9,9]]}}
RULA_B={1:[1,3,2,3,3,4,5,5,6,6,7,7],2:[2,3,2,3,4,5,5,5,6,7,7,7],3:[3,3,3,4,4,5,5,6,6,7,7,7],4:[5,5,5,6,6,7,7,7,7,7,8,8],5:[7,7,7,7,7,8,8,8,8,8,8,8],6:[8,8,8,8,8,8,8,9,9,9,9,9]}
REBA_A={1:[[1,2,3,4],[2,3,4,5],[2,4,5,6],[3,5,6,7],[4,6,7,8]],2:[[1,2,3,4],[3,4,5,6],[4,5,6,7],[5,6,7,8],[6,7,8,9]],3:[[3,3,5,6],[4,5,6,7],[5,6,7,8],[6,7,8,9],[7,8,9,9]]}
REBA_B={1:{1:[1,2,2],2:[1,2,3]},2:{1:[1,2,3],2:[2,3,4]},3:{1:[3,4,5],2:[4,5,5]},4:{1:[4,5,5],2:[5,6,7]},5:{1:[6,7,8],2:[7,8,8]},6:{1:[7,8,8],2:[8,9,9]}}
REBA_C=[None,[None,1,1,1,2,3,3,4,5,6,7,7,7],[None,1,2,2,3,4,4,5,6,6,7,7,8],[None,2,3,3,3,4,5,6,7,7,8,8,8],[None,3,4,4,4,5,6,7,8,8,9,9,9],[None,4,4,4,5,6,7,8,8,9,9,9,9],[None,6,6,6,7,8,8,9,9,10,10,10,10],[None,7,7,7,8,9,9,9,10,10,11,11,11],[None,8,8,8,9,10,10,10,10,10,11,11,11],[None,9,9,9,10,10,10,11,11,11,12,12,12],[None,10,10,10,11,11,11,11,12,12,12,12,12],[None,11,11,11,11,12,12,12,12,12,12,12,12],[None,12,12,12,12,12,12,12,12,12,12,12,12]]

def score_rula(d):
    ua=abs(d['upper']); upper=1 if ua<=20 else 2 if ua<=45 else 3 if ua<=90 else 4
    upper=clamp(upper+d['sh_up']+d['abd']-d['supported'],1,6)
    lower=1 if 60<=d['lower']<=100 else 2; lower=clamp(lower+d['across'],1,3)
    w=1 if d['wrist']<1 else 2 if d['wrist']<=15 else 3; w=clamp(w+d['wdev'],1,4); tw=2 if d['wtwist'] else 1
    pa=RULA_A[upper][lower][w-1][tw-1]; fa=clamp(pa+d['static']+d['force'],1,8)
    n=1 if d['neck']<=10 else 2 if d['neck']<=20 else 3; n=clamp(n+d['ntwist']+d['nside'],1,6)
    t=1 if d['trunk']<1 else 2 if d['trunk']<=20 else 3 if d['trunk']<=60 else 4; t=clamp(t+d['ttwist']+d['tside'],1,6)
    legs=1 if d['legs_ok'] else 2; pb=RULA_B[n][(t-1)*2+(legs-1)]; fb=clamp(pb+d['static']+d['force'],1,7)
    final=RULA_C[fa][fb]
    level='ยอมรับได้' if final<=2 else 'ควรตรวจสอบ' if final<=4 else 'ควรปรับปรุงเร็ว' if final<=6 else 'ควรปรับปรุงทันที'
    return {'final':final,'upper':upper,'lower':lower,'wrist':w,'neck':n,'trunk':t,'A':fa,'B':fb,'level':level}

def score_reba(d):
    n=1 if d['neck']<=20 else 2; n=clamp(n+d['ntwist']+d['nside'],1,3)
    t=1 if d['trunk']<1 else 2 if d['trunk']<=20 else 3 if d['trunk']<=60 else 4; t=clamp(t+d['ttwist']+d['tside'],1,5)
    legs=(1 if d['legs_ok'] else 2)+(2 if d['knee']>60 else 1 if d['knee']>=30 else 0); legs=clamp(legs,1,4)
    A=clamp(REBA_A[n][t-1][legs-1]+d['load']+d['shock'],1,12)
    ua=abs(d['upper']); upper=1 if ua<=20 else 2 if ua<=45 else 3 if ua<=90 else 4; upper=clamp(upper+d['sh_up']+d['abd']-d['supported'],1,6)
    lower=1 if 60<=d['lower']<=100 else 2
    w=1 if d['wrist']<=15 else 2; w=clamp(w+d['wdev']+d['wtwist'],1,3)
    B=clamp(REBA_B[upper][lower][w-1]+d['coupling'],1,12)
    C=REBA_C[A][B]; final=clamp(C+d['static']+d['repeat']+d['rapid'],1,15)
    level='เล็กน้อย' if final<=1 else 'ต่ำ' if final<=3 else 'ปานกลาง' if final<=7 else 'สูง' if final<=10 else 'สูงมาก'
    return {'final':final,'upper':upper,'lower':lower,'wrist':w,'neck':n,'trunk':t,'A':A,'B':B,'C':C,'level':level}

def show_ref(part, method):
    """แสดงเกณฑ์เป็น HTML เพื่อให้ภาษาไทยใช้ฟอนต์ของเบราว์เซอร์ ไม่ถูกวาดด้วย PIL"""
    labels_map = {
        'แขนส่วนบน': ['≤20°', '20–45°', '45–90°', '>90°'],
        'แขนส่วนล่าง': ['60–100°', 'นอกช่วง 60–100°'],
        'ข้อมือ': ['0–15°', '>15°', 'เบี่ยง/บิด +1'],
        'คอ': ['0–10°', '10–20°', '>20°', 'บิด/เอียง +1'],
        'ลำตัว': ['0°', '0–20°', '20–60°', '>60°', 'บิด/เอียง +1'],
        'ขา': ['สมดุล/รองรับดี', 'ไม่สมดุล', 'เข่างอ 30–60°', 'เข่างอ >60°'],
    }
    labels = labels_map.get(part, ['ใช้ตารางคะแนนด้านล่าง'])
    st.caption(f'{method} — เกณฑ์ประเมิน {part}')
    cols = st.columns(len(labels))
    for col, label in zip(cols, labels):
        col.markdown(
            f"""
            <div style="
                min-height:92px;
                display:flex;
                align-items:center;
                justify-content:center;
                text-align:center;
                padding:10px 8px;
                border:2px solid #3b82f6;
                border-radius:12px;
                background:#eff6ff;
                color:#111827;
                font-size:15px;
                line-height:1.45;
                font-family:'Leelawadee UI','Noto Sans Thai',Tahoma,Arial,sans-serif;
            "><b>{label}</b></div>
            """,
            unsafe_allow_html=True,
        )

def angle(a,b,c):
    a=np.array(a[:2]); b=np.array(b[:2]); c=np.array(c[:2]); ba=a-b; bc=c-b
    v=np.dot(ba,bc)/(np.linalg.norm(ba)*np.linalg.norm(bc)+1e-9); return float(np.degrees(np.arccos(np.clip(v,-1,1))))
def analyze(img):
    import mediapipe as mp
    arr=np.array(img.convert('RGB')); pose=mp.solutions.pose.Pose(static_image_mode=True,model_complexity=1,min_detection_confidence=.5)
    res=pose.process(arr); pose.close()
    if not res.pose_landmarks: raise ValueError('AI ไม่พบร่างกายชัดพอ กรุณาใช้ภาพด้านข้างที่เห็นศีรษะ ลำตัว แขน และขา')
    lm=res.pose_landmarks.landmark
    L=mp.solutions.pose.PoseLandmark
    def p(i): q=lm[i.value]; return (q.x,q.y,q.visibility)
    def side(prefix):
        S=L.LEFT_SHOULDER if prefix=='L' else L.RIGHT_SHOULDER; E=L.LEFT_ELBOW if prefix=='L' else L.RIGHT_ELBOW; W=L.LEFT_WRIST if prefix=='L' else L.RIGHT_WRIST
        H=L.LEFT_HIP if prefix=='L' else L.RIGHT_HIP; K=L.LEFT_KNEE if prefix=='L' else L.RIGHT_KNEE; A=L.LEFT_ANKLE if prefix=='L' else L.RIGHT_ANKLE; I=L.LEFT_INDEX if prefix=='L' else L.RIGHT_INDEX
        sh,el,wr,hi,kn,an,ind=map(p,[S,E,W,H,K,A,I])
        return {'upper':round(abs(180-angle(el,sh,hi)),1),'lower':round(angle(sh,el,wr),1),'wrist':round(abs(180-angle(el,wr,ind)),1),'trunk':round(abs(180-angle(sh,hi,(hi[0],hi[1]+.2,1))),1),'knee':round(abs(180-angle(hi,kn,an)),1),'confidence':round(np.mean([x[2] for x in [sh,el,wr,hi,kn,an]]),2)}
    left,right=side('L'),side('R'); best=left if left['confidence']>=right['confidence'] else right
    best['neck']=10.0
    return left,right,best

meta1,meta2,meta3=st.columns(3)
with meta1: method=st.selectbox('วิธีประเมิน',['RULA','REBA'])
with meta2: student=st.text_input('ชื่อผู้ประเมิน')
with meta3: task=st.text_input('งาน/สถานีงาน')

def stage(stage_key,label):
    st.header(label)
    up=st.file_uploader('อัปโหลดภาพ JPG/PNG',type=['jpg','jpeg','png'],key=f'up_{stage_key}')
    if up:
        img=Image.open(up).convert('RGB'); st.image(img,width=520)
        if st.button('🤖 ให้ AI ช่วยวัดมุม',key=f'ai_{stage_key}'):
            try:
                left,right,best=analyze(img); st.session_state[f'angles_{stage_key}']=best; st.success(f"AI เลือกด้านที่เห็นชัดกว่า (confidence {best['confidence']})")
            except Exception as e: st.error(str(e))
    vals=st.session_state.get(f'angles_{stage_key}',{})
    def num(k,label,default=0): return st.number_input(label,0.0,180.0,float(vals.get(k,default)),1.0,key=f'{stage_key}_{k}')
    d={}
    c1,c2=st.columns(2)
    with c1:
        st.subheader('1. แขนส่วนบน'); show_ref('แขนส่วนบน',method); d['upper']=num('upper','มุมแขนส่วนบน (°)'); d['sh_up']=int(st.checkbox('ยกไหล่',key=f'{stage_key}_sh')); d['abd']=int(st.checkbox('กางแขน',key=f'{stage_key}_abd')); d['supported']=int(st.checkbox('มีที่รองรับแขน',key=f'{stage_key}_sup'))
        st.subheader('2. แขนส่วนล่าง'); show_ref('แขนส่วนล่าง',method); d['lower']=num('lower','มุมข้อศอก (°)',90); d['across']=int(st.checkbox('ปลายแขนไขว้แนวกึ่งกลาง',key=f'{stage_key}_cross'))
        st.subheader('3. ข้อมือ'); show_ref('ข้อมือ',method); d['wrist']=num('wrist','มุมข้อมือ (°)'); d['wdev']=int(st.checkbox('ข้อมือเบี่ยง',key=f'{stage_key}_wdev')); d['wtwist']=int(st.checkbox('ข้อมือบิด',key=f'{stage_key}_wtw'))
    with c2:
        st.subheader('4. คอ'); show_ref('คอ',method); d['neck']=num('neck','มุมคอ (°)',10); d['ntwist']=int(st.checkbox('คอบิด',key=f'{stage_key}_nt')); d['nside']=int(st.checkbox('คอเอียง',key=f'{stage_key}_ns'))
        st.subheader('5. ลำตัว'); show_ref('ลำตัว',method); d['trunk']=num('trunk','มุมลำตัว (°)'); d['ttwist']=int(st.checkbox('ลำตัวบิด',key=f'{stage_key}_tt')); d['tside']=int(st.checkbox('ลำตัวเอียง',key=f'{stage_key}_ts'))
        st.subheader('6. ขา'); show_ref('ขา',method); d['legs_ok']=st.checkbox('ขา/เท้ารองรับและสมดุล',value=True,key=f'{stage_key}_legs'); d['knee']=num('knee','มุมงอเข่า (°)')
    if method=='RULA':
        d['static']=int(st.checkbox('ค้างท่า ≥1 นาที หรือทำซ้ำ ≥4 ครั้ง/นาที',key=f'{stage_key}_stat')); d['force']=st.selectbox('แรง/น้ำหนัก',['0 — <2 กก.','1 — 2–10 กก.','2 — 2–10 กก. ค้าง/ซ้ำ','3 — >10 กก./แรงกระชาก'],key=f'{stage_key}_force'); d['force']=int(d['force'][0]); res=score_rula(d)
        st.subheader('ตาราง A / B / C'); st.table([{'กลุ่ม':'A แขนและข้อมือ','คะแนน':res['A']},{'กลุ่ม':'B คอ ลำตัว ขา','คะแนน':res['B']},{'กลุ่ม':'C คะแนนสุดท้าย','คะแนน':res['final']}])
    else:
        d['load']=st.selectbox('Load/Force',[0,1,2],key=f'{stage_key}_load'); d['shock']=int(st.checkbox('มีแรงกระแทก/แรงเพิ่มเร็ว',key=f'{stage_key}_shock')); d['coupling']=st.selectbox('คุณภาพการจับชิ้นงาน',[0,1,2,3],key=f'{stage_key}_couple'); d['static']=int(st.checkbox('ค้างท่า >1 นาที',key=f'{stage_key}_static')); d['repeat']=int(st.checkbox('ทำซ้ำ >4 ครั้ง/นาที',key=f'{stage_key}_rep')); d['rapid']=int(st.checkbox('เปลี่ยนท่ามาก/เร็ว',key=f'{stage_key}_rapid')); res=score_reba(d)
        st.subheader('ตาราง A / B / C'); st.table([{'ตาราง':'A','คะแนน':res['A']},{'ตาราง':'B','คะแนน':res['B']},{'ตาราง':'C','คะแนน':res['C']},{'ตาราง':'คะแนนสุดท้าย','คะแนน':res['final']}])
    st.metric(f'คะแนน {method} สุดท้าย',res['final']); st.info(f"ระดับความเสี่ยง: {res['level']}")
    st.session_state[f'res_{stage_key}']=res
    return res

t1,t2,t3=st.tabs(['ก่อนปรับปรุง','หลังปรับปรุง','สรุป'])
with t1: before=stage('before','ก่อนปรับปรุง')
with t2: after=stage('after','หลังปรับปรุง')
with t3:
    b=st.session_state.get('res_before'); a=st.session_state.get('res_after')
    if b and a:
        st.subheader('สรุปผลก่อน–หลัง')
        st.table([{'ช่วง':'ก่อนปรับปรุง','คะแนน':b['final'],'ระดับ':b['level']},{'ช่วง':'หลังปรับปรุง','คะแนน':a['final'],'ระดับ':a['level']}])
        st.metric('การเปลี่ยนแปลงคะแนน',a['final']-b['final'])
        st.caption('ไม่คำนวณเป็นเปอร์เซ็นต์ เพราะคะแนน RULA/REBA เป็น ordinal risk score')
        payload={'method':method,'student':student,'task':task,'date':str(date.today()),'before':b,'after':a}
        st.download_button('ดาวน์โหลดผล JSON',json.dumps(payload,ensure_ascii=False,indent=2).encode('utf-8'),'rula_reba_result.json','application/json')
    else: st.info('กรอกผลก่อนและหลังปรับปรุงก่อน')

st.divider()
st.caption('สำหรับการเรียนการสอนและการคัดกรองเบื้องต้น ไม่ใช่เครื่องมือวินิจฉัยทางการแพทย์')
