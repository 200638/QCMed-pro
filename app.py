import streamlit as st
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="منصة QCM الطبية", layout="wide")

# تهيئة حالة الجلسة (Session State) لحفظ البيانات مؤقتاً
if 'users_db' not in st.session_state:
    st.session_state.users_db = [] # لتخزين طلبات الدفع
if 'shared_qcms' not in st.session_state:
    st.session_state.shared_qcms = [] # بنك الامتحانات المشتركة بين الطلاب

st.title("📚 منصة التدريب الطبي والتنافسي (QCM)")

# القائمة الجانبية للتنقل
menu = st.sidebar.selectbox("القائمة الرئيسية", ["التسجيل والاشتراك", "تصفح المقررات (Unité/Module)", "بنك امتحانات الكلية والمشاركة", "لوحة تحكم الأدمن"])

# ---------------------------------------------------------
# 1. قسم التسجيل والدفع (CCP / BaridiMob)
# ---------------------------------------------------------
if menu == "التسجيل والاشتراك":
    st.header("تسجيل الدفع والاشتراك")
    st.info("قم بتحويل المبلغ عبر بريد الجزائر (CCP) واقترح بياناتك مع صورة وصل الدفع.")

    with st.form("payment_form"):
        # فصل الاسم عن رقم الهاتف كما طلبتِ بدقة
        student_name = st.text_input("الاسم واللقب")
        phone_number = st.text_input("رقم الهاتف")
        
        # خيارات الاشتراك (شهري أو سنوي)
        subscription_type = st.selectbox("نوع الاشتراك", ["اشتراك شهري", "اشتراك سنوي"])
        
        # رفع صورة وصل الدفع (إلزامي)
        receipt_image = st.file_uploader("صورة وصل الدفع (CCP)", type=["jpg", "png", "jpeg"])
        
        submit_button = st.form_submit_button("إرسال طلب الاشتراك")

        if submit_button:
            if student_name and phone_number and receipt_image:
                # حفظ الطلب في قاعدة البيانات المؤقتة
                request_data = {
                    "name": student_name,
                    "phone": phone_number,
                    "type": subscription_type,
                    "image": receipt_image,
                    "status": "معلق"
                }
                st.session_state.users_db.append(request_data)
                st.success("تم إرسال وصل الدفع بنجاح! سيتم مراجعته وتفعيل حسابك قريباً.")
            else:
                    st.error("الرجاء إدخال الاسم، رقم الهاتف، وإرفاق صورة وصل الدفع.")

# ---------------------------------------------------------
# 2. تصفح المقررات (الهيكلة الهرمية + أهم النقاط + الامتحانات)
# ---------------------------------------------------------
elif menu == "تصفح المقررات (Unité/Module)":
    st.header("المقررات الدراسية")
    
    # الهيكلة الهرمية: Unité -> Module -> Cours
    unit_name = st.selectbox("اختر الوحدة الأساسية (Unité)", ["Unité 1: Appareil Cardiovasculaire", "Unité 2: Système Nerveux", "Unité 3: Appareil Respiratoire"])
    module_name = st.text_input("اسم المادة (Module)")
    prof_name = st.text_input("اسم أستاذ المادة (اختياري)")
    
    if module_name:
        st.subheader(f"محتوى مادة: {module_name}")
        
        # قسم النقاط الهامة لكل Module
        st.markdown("---")
        st.markdown("### 📌 أهم النقاط التي ركزت عليها الامتحانات السابقة:")
        st.info("هنا تظهر الخلاصة وأبرز الأجزاء المتكررة في امتحانات السنوات الفائطة لتلك المادة.")
        
        cours_name = st.text_input("عنوان الدرس (Cours)")
        if cours_name:
            st.write(f"تحميل ملفات الدرس الخاص بـ: {cours_name}")
            st.button(f"تحميل درس {cours_name} (PDF/Scan)")
            
            st.markdown("---")
            st.markdown("### 📝 نظام الأسئلة والتصنيف للدرس:")
            qcm_type = st.radio("اختر نوع الأسئلة:", [
                "QCM de votre prof (أسئلة أستاذك)", 
                "QCM de votre faculté (أسئلة الكلية)", 
                "QCM généré par l'IA (بأسلوب أستاذك)"
            ])
            
            # ميزة التحقق من هوية الأستاذ في الامتحانات القديمة
            if "faculté" in qcm_type:
                st.warning("⚠️ هذا الامتحان ليس مرتبطاً حصرياً باسم أستاذك المسجل.")
                is_prof_exam = st.radio("هل امتحان هذه السنة يتبع لأستاذك الخاص؟", ["نعم", "لا أعلم / متأكد بأنه ليس له"])
                if is_prof_exam == "لا أعلم / متأكد بأنه ليس له":
                    st.info("تم اعتباره امتحاناً عاماً للكلية وليس لأستاذك.")
                else:
                    st.success("تم ربطه بأسئلة أستاذك.")

            st.button("بدء اختبار QCM")

# ---------------------------------------------------------
# 3. بنك امتحانات الكلية والمشاركة بين الطلاب
# ---------------------------------------------------------
elif menu == "بنك امتحانات الكلية والمشاركة":
    st.header("بنك الامتحانات الشامل للكلية ومشاركة الـ QCMs")
    
    faculty_name = st.selectbox("اختر كليتك", ["كلية الطب - الجزائر", "كلية الطب - وهران", "كلية الطب - قسنطينة", "كلية الطب - بليدة"])
    
    tab1, tab2 = st.tabs(["📂 تصفح بنك الامتحانات", "📤 مشاركة QCM مع الزملاء"])
    
    with tab1:
        st.subheader(f"امتحانات مأخوذة من قاعدة بيانات: {faculty_name}")
        if st.session_state.shared_qcms:
            for item in st.session_state.shared_qcms:
                if item['faculty'] == faculty_name:
                    st.write(- f"**المادة:** {item['module']} | **أرسله الطالب:** {item['student']}")
                    st.button(f"تحميل امتحان {item['module']}", key=item['module'])
        else:
            st.write("لا توجد امتحانات مرفوعة حالياً لهذه الكلية. كن أول من يشارك!")
            
    with tab2:
        st.subheader("مشاركة ملف QCM أو امتحان مع زملائك")
        with st.form("share_form"):
            s_module = st.text_input("اسم المادة (Module)")
            s_name = st.text_input("اسمك المستعار أو الحقيقي")
            s_file = st.file_uploader("ملف الـ QCM (صورة أو PDF)", type=["pdf", "png", "jpg"])
            s_submit = st.form_submit_button("مشاركة الملف")
            
            if s_submit and s_module and s_file:
                st.session_state.shared_qcms.append({
                    "faculty": faculty_name,
                    "module": s_module,
                    "student": s_name,
                    "file": s_file
                })
                st.success("شكراً لك! تم إضافته إلى بنك امتحانات الكلية بنجاح.")

# ---------------------------------------------------------
# 4. لوحة تحكم الأدمن (Admin Panel)
# ---------------------------------------------------------
elif menu == "لوحة تحكم الأدمن":
    st.header("لوحة تحكم المشرف (Admin Panel)")
    
    admin_pass = st.text_input("كلمة سر الأدمن", type="password")
    
    if admin_pass == "admin123": # كلمة السر التجريبية للأدمن
        st.success("مرحباً بكِ في لوحة التحكم.")
        st.subheader("الطلبات المعلقة للاشتراكات:")
        
        if not st.session_state.users_db:
            st.write("لا توجد طلبات اشتراك معلقة حالياً.")
        else:
            for i, user in enumerate(st.session_state.users_db):
                if user["status"] == "معلق":
                    st.markdown(f"---")
                    # عرض الاسم وحده ورقم الهاتف وحده كما طلبتِ بدقة
                    st.write(f"**الاسم واللقب:** {user['name']}")
                    st.write(f"**رقم الهاتف:** {user['phone']}")
                    st.write(f"**نوع الاشتراك المطلوب:** {user['type']}")
                    
                    # عرض صورة الوصل المالي
                    img = Image.open(user['image'])
                    st.image(img, caption=f"وصل الدفع لـ {user['name']}", width=300)
                    
                    # زر التفعيل المباشر (Activate Premium)
                    if st.button(f"تفعيل الحساب (Activate Premium) لـ {user['name']}", key=f"activate_{i}"):
                        st.session_state.users_db[i]["status"] = "مفعل"
                        st.success(f"تم تفعيل الحساب بنجاح لمدة ({user['type']}) للطالب {user['name']}!")
                        st.rerun()
    elif admin_pass != "":
        st.error("كلمة السر خاطئة.")
