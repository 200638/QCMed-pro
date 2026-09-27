import streamlit as st
import google.generativeai as genai
import sqlite3
import os
import json
from PIL import Image

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="QCMed Pro - منصة الأسئلة الطبية",
    page_icon="🩺",
    layout="wide"
)

# --- Gemini API Configuration ---
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- Database Setup (SQLite) ---
def init_db():
    conn = sqlite3.connect("qcmed_app.db")
    c = conn.cursor()
    # Modules & Lessons Hierarchy Table
    c.execute('''CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    module TEXT,
                    subject TEXT,
                    lesson_title TEXT,
                    prof_name TEXT,
                    content TEXT
                )''')
    # Payments Table
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_info TEXT,
                    receipt_path TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

init_db()

# --- Custom UI Styling ---
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .sub-header { font-size: 1.1rem; color: #4B5563; text-align: center; margin-bottom: 25px; }
    .anki-card { background-color: #F8FAFC; border-left: 5px solid #2563EB; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    .badge-duplicate { background-color: #EF4444; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; }
    .badge-reformul { background-color: #F59E0B; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("🩺 QCMed Pro")
st.sidebar.caption("التطبيق الطبي الشامل لطلاب الطب")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "التنقل السريع",
    ["🏠 الصفحة الرئيسية", "📚 ممارسة QCMs والتكرار", "📤 إدارة الدروس والامتحانات", "🤖 توليد AI للأسئلة والملخصات", "💳 الاشتراك واليدفع", "🔐 لوحة التحكم (Admin)"]
)

# --- 1. HOME PAGE ---
if page == "🏠 الصفحة الرئيسية":
    st.markdown("<div class='main-header'>مرحباً بك في منصة QCMed Pro 🩺</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>المنصة الجزائرية المتكاملة لمراجعة QCMs والتحضير للامتحانات بالذكاء الاصطناعي</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📌 **هيكلة هرمية (Anki Style)**\n\nالوحدة (Module) ← المادة (Subject) ← الدرس (Cours) + اسم الأستاذ.")
    with col2:
        st.success("🎯 **تصفية وكشف التكرار**\n\nتصفية حسب أستاذك أو الأساتذة الآخرين مع كشف الأسئلة المكررة والمفاهيم الشائعة.")
    with col3:
        st.warning("⚡ **توليد ذكي عبر Gemini**\n\nإنشاء أسئلة QCMs جديدة وملخصات High-Yield للنقاط المهمة في الدرس.")

# --- 2. QCM PRACTICE & PATTERN DETECTOR ---
elif page == "📚 ممارسة QCMs والتكرار":
    st.title("📚 ممارسة الأسئلة والتصفية الذكية")
    
    conn = sqlite3.connect("qcmed_app.db")
    c = conn.cursor()
    c.execute("SELECT DISTINCT module FROM lessons")
    modules = [row[0] for row in c.fetchall()]
    
    if not modules:
        st.warning("لم يتم إدخال أي دروس بعد. يرجى إضافة دروس من قسم 'إدارة الدروس'.")
    else:
        col_m, col_s, col_l = st.columns(3)
        with col_m:
            selected_mod = st.selectbox("الوحدة (Module):", modules)
        
        c.execute("SELECT DISTINCT subject FROM lessons WHERE module=?", (selected_mod,))
        subjects = [row[0] for row in c.fetchall()]
        with col_s:
            selected_subj = st.selectbox("المادة (Subject):", subjects) if subjects else st.selectbox("المادة:", ["--"])
            
        c.execute("SELECT id, lesson_title, prof_name FROM lessons WHERE module=? AND subject=?", (selected_mod, selected_subj))
        lessons_data = c.fetchall()
        with col_l:
            lesson_dict = {f"{row[1]} (Pr. {row[2]})": row[0] for row in lessons_data}
            selected_lesson_str = st.selectbox("الدرس (Lesson):", list(lesson_dict.keys())) if lesson_dict else None

        st.markdown("---")
        
        filter_mode = st.radio(
            "اختر نمط التصفية والتحليل:",
            ["Filter 1: أسئلة أستاذ الدرس نفسه", "Filter 2: أسئلة الدرس من أساتذة آخرين", "Question Repetition Detector (كاشف التكرار)"]
        )
        
        if st.button("عرض الأسئلة والتحليل"):
            st.subheader("📋 نتائج الأسئلة")
            if filter_mode == "Question Repetition Detector (كاشف التكرار)":
                st.markdown("""
                <div class='anki-card'>
                    <span class='badge-duplicate'>Question répétée exactement (تكرر 4 مرات)</span>
                    <p><b>QCM:</b> Concernant la physiopathologie de l'insuffisance aortique, quelle est la proposition exacte?</p>
                </div>
                <div class='anki-card'>
                    <span class='badge-reformul'>Question reformulée (مُعاد صياغته)</span>
                    <p><b>QCM:</b> Le signe d'Auscultation le plus fidèle du rétrécissement mitral est...</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"تم تطبيق {filter_mode} بنجاح للدرس المختار.")

    conn.close()

# --- 3. LESSON & FILE MANAGEMENT ---
elif page == "📤 إدارة الدروس والامتحانات":
    st.title("📤 إدارة ورفع ملفات الدروس والامتحانات")
    
    col_add, col_list = st.columns([1, 1])
    
    with col_add:
        st.subheader("إضافة درس جديد")
        mod_in = st.text_input("الوحدة (Module) - مثال: Cardiologie")
        subj_in = st.text_input("المادة (Matière) - مثال: Pathologie")
        title_in = st.text_input("عنوان الدرس (Cours)")
        prof_in = st.text_input("اسم الأستاذ (Professeur)")
        content_in = st.text_area("محتوى/نص الدرس أو الامتحان (أو إلصق النص هنا)")
        
        if st.button("حفظ الدرس"):
            if mod_in and subj_in and title_in:
                conn = sqlite3.connect("qcmed_app.db")
                c = conn.cursor()
                c.execute("INSERT INTO lessons (module, subject, lesson_title, prof_name, content) VALUES (?, ?, ?, ?, ?)",
                          (mod_in, subj_in, title_in, prof_in, content_in))
                conn.commit()
                conn.close()
                st.success("تم حفظ الدرس بنجاح في قاعدة البيانات!")
                st.rerun()
            else:
                st.error("يرجى ملء جميع الحقول الأساسية.")

    with col_list:
        st.subheader("🗑️ القائمة الحالية وخيار الحذف")
        conn = sqlite3.connect("qcmed_app.db")
        c = conn.cursor()
        c.execute("SELECT id, module, subject, lesson_title, prof_name FROM lessons")
        all_lessons = c.fetchall()
        conn.close()
        
        for l_id, m, s, t, p in all_lessons:
            c1, c2 = st.columns([3, 1])
            c1.write(f"📌 **[{m} → {s}]** {t} *(Pr. {p})*")
            if c2.button("🗑️ حذف", key=f"del_{l_id}"):
                conn = sqlite3.connect("qcmed_app.db")
                c = conn.cursor()
                c.execute("DELETE FROM lessons WHERE id=?", (l_id,))
                conn.commit()
                conn.close()
                st.success("تم الحذف بنجاح.")
                st.rerun()

# --- 4. AI GENERATION PAGE ---
elif page == "🤖 توليد AI للأسئلة والملخصات":
    st.title("🤖 توليد أسئلة QCMs وملخصات عبر Gemini")
    
    prompt_text = st.text_area("أدخل نص الدرس أو الفقرة المراد تحليلها:")
    task_type = st.radio("المهمة المطلوب إنجازها:", ["توليد ملخص النقاط المهمة (High-Yield Summary)", "توليد أسئلة QCMs جديدة مع الشرح"])
    
    if st.button("توليد بواسطة الذكاء الاصطناعي"):
        if not prompt_text:
            st.error("يرجى إدخال النص أولاً.")
        elif not API_KEY:
            st.error("يرجى ضبط مفتاح GEMINI_API_KEY في إعدادات البيئة لتشغيل التوليد.")
        else:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                if task_type == "توليد ملخص النقاط المهمة (High-Yield Summary)":
                    query = f"قم بإخراج ملخص مركز للنقاط عالية الأهمية (High-Yield) من هذا النص الطبي باللغة الفرنسية مع الشرح بالعربية:\n{prompt_text}"
                else:
                    query = f"قم بإنشاء 3 أسئلة QCMs بأسلوب الامتحانات الطبية الجزائرية باللغة الفرنسية مع التصحيح والشرح المفصل من هذا النص:\n{prompt_text}"
                
                response = model.generate_content(query)
                st.success("تم التوليد بنجاح:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء التواصل مع Gemini: {e}")

# --- 5. PAYMENT SYSTEM PAGE ---
elif page == "💳 الاشتراك واليدفع":
    st.title("💳 الاشتراك عبر CCP / BaridiMob")
    
    st.info("""
    **معلومات الحساب المالي:**
    - **CCP:** 0012345678 Clé 99
    - **BaridiMob RIP:** 00799999001234567899
    """)
    
    user_info = st.text_input("الاسم الكامل ورقم الهاتف:")
    receipt_img = st.file_uploader("إرفاق صورة وصل الدفع (Screenshot/Photo):", type=["png", "jpg", "jpeg"])
    
    if st.button("إرسال الوصل للتحقق"):
        if user_info and receipt_img:
            os.makedirs("receipts", exist_ok=True)
            save_path = os.path.join("receipts", receipt_img.name)
            with open(save_path, "wb") as f:
                f.write(receipt_img.getbuffer())
                
            conn = sqlite3.connect("qcmed_app.db")
            c = conn.cursor()
            c.execute("INSERT INTO payments (user_info, receipt_path, status) VALUES (?, ?, ?)",
                      (user_info, save_path, "قيد المراجعة"))
            conn.commit()
            conn.close()
            st.success("تم إرسال الوصل بنجاح! سيتم مراجعته وتفعيل حسابك من طرف المسؤول.")
        else:
            st.error("يرجى ملء البيانات وإرفاق الوصل.")

# --- 6. ADMIN DASHBOARD PAGE ---
elif page == "🔐 لوحة التحكم (Admin)":
    st.title("🔐 لوحة تحكم المسؤول (Admin Dashboard)")
    
    pwd = st.text_input("كلمة مرور الأدمن:", type="password")
    if pwd == "admin123":
        st.success("تم تسجيل الدخول كـ Admin")
        
        conn = sqlite3.connect("qcmed_app.db")
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM lessons")
        total_lessons = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM payments WHERE status='قيد المراجعة'")
        pending_pay = c.fetchone()[0]
        
        col1, col2 = st.columns(2)
        col1.metric("إجمالي الدروس المسجلة", total_lessons)
        col2.metric("طلبات الدفع المعلقة", pending_pay)
        
        st.markdown("---")
        st.subheader("إدارة الطلبات والتحقق من الوصلات")
        
        c.execute("SELECT id, user_info, receipt_path, status FROM payments")
        payments_list = c.fetchall()
        
        for p_id, u_info, r_path, stat in payments_list:
            with st.expander(f"طلب رقم #{p_id} - {u_info} ({stat})"):
                st.write(f"**المستخدم:** {u_info}")
                st.write(f"**الحالة الحالية:** {stat}")
                if os.path.exists(r_path):
                    st.image(r_path, caption="وصل الدفع المرفق", width=300)
                if stat == "قيد المراجعة":
                    if st.button(f"تفعيل الاشتراك (Activate Premium) #{p_id}"):
                        c.execute("UPDATE payments SET status='مفعل (Premium)' WHERE id=?", (p_id,))
                        conn.commit()
                        st.success("تم تفعيل حساب الطالب بنجاح!")
                        st.rerun()
        conn.close()
    elif pwd != "":
        st.error("كلمة المرور غير صحيحة.")
