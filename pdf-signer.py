import os
import glob
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_stamp_pdf(seal_path, output_temp_path, x, y, width, height, text=None, text_y_offset=0):
    """
    إنشاء ملف PDF مؤقت يحتوي على صورة الختم ونص ديناميكي
    """
    c = canvas.Canvas(output_temp_path, pagesize=letter)
    
    # رسم صورة الختم
    c.drawImage(seal_path, x, y, width=width, height=height)
    
    # إضافة نص ديناميكي إذا وجد
    if text:
        text_y = y + text_y_offset  # تحديد موقع النص بالنسبة للختم
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, text_y, text)
    
    c.save()

def apply_stamp_to_pdf(pdf_path, stamp_pdf_path, output_path, page_number=0):
    """
    تطبيق الختم على ملف PDF الأصلي
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    stamp_reader = PdfReader(stamp_pdf_path)
    stamp_page = stamp_reader.pages[0]

    for i, page in enumerate(reader.pages):
        if i == page_number:
            page.merge_page(stamp_page)
        writer.add_page(page)

    with open(output_path, 'wb') as f:
        writer.write(f)

def get_invoice_files(directory_path):
    """الحصول على جميع ملفات PDF في المجلد مع معالجة الأخطاء"""
    try:
        if not os.path.exists(directory_path):
            print(f"❌ المجلد غير موجود: {directory_path}")
            return []
        
        # البحث عن جميع ملفات PDF بطرق مختلفة
        pdf_files = []
        
        # الطريقة 1: استخدام glob
        pdf_pattern = os.path.join(directory_path, "*.pdf")
        pdf_files = glob.glob(pdf_pattern)
        
        # الطريقة 2: إذا لم يعثر على ملفات، جرب البحث الحساس وغير الحساس للحروف
        if not pdf_files:
            all_files = os.listdir(directory_path)
            pdf_files = [os.path.join(directory_path, f) for f in all_files 
                        if f.lower().endswith('.pdf')]
        
        return pdf_files
        
    except Exception as e:
        print(f"❌ خطأ في الوصول للمجلد: {e}")
        return []

def display_folder_contents(directory_path):
    """عرض محتويات المجلد للمساعدة في التشخيص"""
    try:
        if not os.path.exists(directory_path):
            print(f"المجلد غير موجود: {directory_path}")
            return
        
        print(f"\n📂 محتويات مجلد '{directory_path}':")
        print("-" * 50)
        
        items = os.listdir(directory_path)
        if not items:
            print("المجلد فارغ")
            return
            
        for item in items:
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                print(f"📄 {item} ({size} bytes)")
            else:
                print(f"📁 {item} (مجلد)")
                
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ لا يمكن عرض محتويات المجلد: {e}")

def process_invoice_pdfs(input_directory, output_directory, stamp_image_path, company_name, position_settings=None):
    """
    معالجة جميع فواتير PDF في المجلد المحدد
    """
    
    # الإعدادات الافتراضية لموقع الختم
    if position_settings is None:
        position_settings = {
            'stamp_x': 400,
            'stamp_y': 40,
            'stamp_width': 150,
            'stamp_height': 100,
            'text_y_offset': -20
        }
    
    # إنشاء مجلد الإخراج إذا لم يكن موجوداً
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"✅ تم إنشاء مجلد الإخراج: {output_directory}")
    
    # التحقق من وجود صورة الختم
    if not os.path.exists(stamp_image_path):
        print(f"❌ صورة الختم غير موجودة: {stamp_image_path}")
        return []
    
    # عرض محتويات المجلد للمساعدة في التشخيص
    display_folder_contents(input_directory)
    
    # الحصول على جميع ملفات PDF
    pdf_files = get_invoice_files(input_directory)
    
    if not pdf_files:
        print(f"\n❌ لم يتم العثور على أي ملفات PDF في المجلد: {input_directory}")
        print("يرجى التأكد من:")
        print("1. وجود ملفات PDF في المجلد المحدد")
        print("2. أن الملفات لها امتداد .pdf")
        print("3. أن المسار صحيح")
        return []
    
    print(f"\n📁 تم العثور على {len(pdf_files)} ملف PDF للمعالجة:")
    for pdf_file in pdf_files:
        print(f"   - {os.path.basename(pdf_file)}")
    
    processed_files = []
    
    for pdf_file in pdf_files:
        try:
            # استخراج اسم الملف بدون extension
            file_name = os.path.splitext(os.path.basename(pdf_file))[0]
            
            # إنشاء اسم للملف المخرج
            output_file_name = f"{file_name}_signed.pdf"
            output_file_path = os.path.join(output_directory, output_file_name)
            
            # إنشاء مسار للملف المؤقت للختم
            temp_stamp_pdf = os.path.join(output_directory, f"temp_stamp_{file_name}.pdf")
            
            # النص الديناميكي للختم
            stamp_text = f"{company_name}"
            
            print(f"\n🔄 جاري معالجة: {os.path.basename(pdf_file)}")
            
            # 1. إنشاء ملف الختم المؤقت
            create_stamp_pdf(
                stamp_image_path, 
                temp_stamp_pdf, 
                position_settings['stamp_x'],
                position_settings['stamp_y'],
                position_settings['stamp_width'],
                position_settings['stamp_height'],
                text=stamp_text,
                text_y_offset=position_settings['text_y_offset']
            )
            
            # 2. تطبيق الختم على الفاتورة
            apply_stamp_to_pdf(pdf_file, temp_stamp_pdf, output_file_path)
            
            # 3. تنظيف الملف المؤقت
            if os.path.exists(temp_stamp_pdf):
                os.remove(temp_stamp_pdf)
            
            processed_files.append(output_file_name)
            print(f"✅ تم توقيع: {output_file_name}")
            
        except Exception as e:
            print(f"❌ خطأ في معالجة {pdf_file}: {e}")
    
    return processed_files

def main():
    """الدالة الرئيسية"""
    
    # الإعدادات - يمكن تعديلها حسب الحاجة
    SETTINGS = {
        'input_directory': 'C:/Users/Dell/OneDrive/Desktop/tech-files/edit-pdf/invoices',
        'output_directory': 'C:/Users/Dell/OneDrive/Desktop/tech-files/edit-pdf/signed_invoices',
        'stamp_image_path': 'C:/Users/Dell/OneDrive/Desktop/tech-files/edit-pdf/stamp-blue.png',
        'company_name': 'Mazda specialist Center ',
        
        # إعدادات موقع الختم (يمكن تعديلها حسب تخطيط الفاتورة)
        'position_settings': {
            'stamp_x': 400,        # الإحداثي الأفقي
            'stamp_y': 50,         # الإحداثي الرأسي
            'stamp_width': 150,    # عرض الختم
            'stamp_height': 100,   # ارتفاع الختم
            'text_y_offset': -20   # موقع النص تحت الختم
        }
    }
    
    print("🚀 بدء عملية توقيع الفواتير تلقائياً...")
    print("=" * 60)
    
    # معالجة جميع الفواتير
    processed_files = process_invoice_pdfs(
        SETTINGS['input_directory'],
        SETTINGS['output_directory'],
        SETTINGS['stamp_image_path'],
        SETTINGS['company_name'],
        SETTINGS['position_settings']
    )
    
    print("\n" + "=" * 60)
    if processed_files:
        print(f"🎉 تم الانتهاء من معالجة {len(processed_files)} ملف بنجاح!")
        print("📂 الملفات المعالجة:")
        for file in processed_files:
            print(f"   ✓ {file}")
    else:
        print("⚠️ لم يتم معالجة أي ملف")

# استخدام تفاعلي لإنشاء المجلدات إذا لم تكن موجودة
def setup_folders():
    """إعداد المجلدات المطلوبة"""
    folders = [
        'C:/Users/Dell/OneDrive/Desktop/tech-files/edit-pdf/invoices',
        'C:/Users/Dell/OneDrive/Desktop/tech-files/edit-pdf/signed_invoices'
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ تم إنشاء المجلد: {folder}")
        else:
            print(f"📁 المجلد موجود مسبقاً: {folder}")

if __name__ == "__main__":
    # أولاً: إعداد المجلدات
    print("🔧 التحضير والإعداد...")
    setup_folders()
    
    # ثانياً: تشغيل البرنامج الرئيسي
    main()
    
    # نصائح إضافية
    print("\n💡 نصائح:")
    print("1. ضع ملفات PDF في مجلد 'invoices'")
    print("2. تأكد من وجود صورة الختم 'stamp-blue.png'")
    print("3. الملفات الموقعة ستظهر في مجلد 'signed_invoices'")