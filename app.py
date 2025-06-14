from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  

MAJORS_DATA = {
    "FEB1": {
        "name": "Akuntansi",
        "faculty": "Fakultas Ekonomi dan Bisnis",
        "riasec": "CI",
        "description": "Mengolah data keuangan dan laporan akuntansi dengan ketelitian tinggi"
    },
    "FEB2": {
        "name": "Manajemen",
        "faculty": "Fakultas Ekonomi dan Bisnis",
        "riasec": "EC",
        "description": "Mengelola organisasi dan sumber daya untuk mencapai tujuan bisnis"
    },
    "FEB3": {
        "name": "Ekonomi Pembangunan",
        "faculty": "Fakultas Ekonomi dan Bisnis",
        "riasec": "IE",
        "description": "Menganalisis kebijakan ekonomi dan pembangunan masyarakat"
    },
    "FEB4": {
        "name": "Kewirausahaan",
        "faculty": "Fakultas Ekonomi dan Bisnis",
        "riasec": "EC",
        "description": "Mengembangkan inovasi bisnis dan menciptakan peluang usaha"
    },
    "FIB1": {
        "name": "Bahasa Mandarin",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "AS",
        "description": "Mempelajari bahasa, budaya, dan sastra Tiongkok"
    },
    "FIB2": {
        "name": "Etnomusikologi",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "AI",
        "description": "Meneliti musik tradisional dan budaya musik berbagai etnis"
    },
    "FIB3": {
        "name": "Ilmu Sejarah",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "IA",
        "description": "Mengkaji peristiwa masa lalu dan perkembangan peradaban"
    },
    "FIB4": {
        "name": "Perpustakaan dan Sains Informasi",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "CI",
        "description": "Mengelola informasi dan sistem perpustakaan digital"
    },
    "FIB5": {
        "name": "Sastra Arab",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "AS",
        "description": "Mempelajari bahasa, sastra, dan budaya Arab"
    },
    "FIB6": {
        "name": "Sastra Batak",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "AS",
        "description": "Mempelajari bahasa, sastra, dan budaya Batak"
    },
    "FIB7": {
        "name": "Sastra Indonesia",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "AS",
        "description": "Mempelajari bahasa dan sastra Indonesia"
    },
    "FIB8": {
        "name": "Sastra Inggris",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "AS",
        "description": "Mempelajari bahasa, sastra, dan budaya Inggris"
    },
    "FIB9": {
        "name": "Sastra Jepang",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "AS",
        "description": "Mempelajari bahasa, sastra, dan budaya Jepang"
    },
    "FIB10": {
        "name": "Sastra Melayu",
        "faculty": "Fakultas Ilmu Budaya",
        "riasec": "AS",
        "description": "Mempelajari bahasa, sastra, dan budaya Melayu"
    },
    "FISIP1": {
        "name": "Sosiologi",
        "faculty": "Fakultas Ilmu Sosial dan Ilmu Politik",
        "riasec": "IS",
        "description": "Mengkaji struktur dan dinamika masyarakat"
    },
    "FISIP2": {
        "name": "Ilmu Politik",
        "faculty": "Fakultas Ilmu Sosial dan Ilmu Politik",
        "riasec": "IE",
        "description": "Menganalisis sistem politik dan kebijakan publik"
    },
    "FISIP3": {
        "name": "Ilmu Komunikasi",
        "faculty": "Fakultas Ilmu Sosial dan Ilmu Politik",
        "riasec": "SE",
        "description": "Mempelajari proses komunikasi dan media massa"
    },
    "FISIP4": {
        "name": "Ilmu Kesejahteraan Sosial",
        "faculty": "Fakultas Ilmu Sosial dan Ilmu Politik",
        "riasec": "SI",
        "description": "Mengembangkan program kesejahteraan masyarakat"
    },
    "FISIP5": {
        "name": "Ilmu Administrasi Bisnis",
        "faculty": "Fakultas Ilmu Sosial dan Ilmu Politik",
        "riasec": "EC",
        "description": "Mengelola administrasi dan operasional bisnis"
    },
    "FISIP6": {
        "name": "Ilmu Administrasi Publik",
        "faculty": "Fakultas Ilmu Sosial dan Ilmu Politik",
        "riasec": "ES",
        "description": "Mengelola administrasi pemerintahan dan pelayanan publik"
    },
    "FISIP7": {
        "name": "Antropologi Sosial",
        "faculty": "Fakultas Ilmu Sosial dan Ilmu Politik",
        "riasec": "IS",
        "description": "Mengkaji budaya dan perilaku masyarakat"
    },
    "FH1": {
        "name": "Ilmu Hukum",
        "faculty": "Fakultas Hukum",
        "riasec": "ISE",
        "description": "Mempelajari sistem hukum dan praktik peradilan"
    },
    "FPSI1": {
        "name": "Psikologi",
        "faculty": "Fakultas Psikologi",
        "riasec": "SI",
        "description": "Mempelajari perilaku dan proses mental manusia"
    },
    "FK1": {
        "name": "Pendidikan Dokter",
        "faculty": "Fakultas Kedokteran",
        "riasec": "ISR",
        "description": "Mempelajari ilmu kedokteran dan praktik medis"
    },
    "FP1": {
        "name": "Agroteknologi",
        "faculty": "Fakultas Pertanian",
        "riasec": "RI",
        "description": "Mengembangkan teknologi pertanian dan produksi tanaman"
    },
    "FP2": {
        "name": "Agribisnis",
        "faculty": "Fakultas Pertanian",
        "riasec": "EC",
        "description": "Mengelola bisnis dan pemasaran produk pertanian"
    },
    "FP3": {
        "name": "Peternakan",
        "faculty": "Fakultas Pertanian",
        "riasec": "RI",
        "description": "Mengelola peternakan dan produksi hewan"
    },
    "FP4": {
        "name": "Teknologi Pangan",
        "faculty": "Fakultas Pertanian",
        "riasec": "IR",
        "description": "Mengembangkan teknologi pengolahan makanan"
    },
    "FP5": {
        "name": "Teknik Pertanian dan Biosistem",
        "faculty": "Fakultas Pertanian",
        "riasec": "RI",
        "description": "Mengembangkan sistem mekanisasi pertanian"
    },
    "FP6": {
        "name": "Manajemen Sumber Daya Perairan",
        "faculty": "Fakultas Pertanian",
        "riasec": "RI",
        "description": "Mengelola sumber daya perikanan dan kelautan"
    },
    "FKG1": {
        "name": "Kedokteran Gigi",
        "faculty": "Fakultas Kedokteran Gigi",
        "riasec": "IRS",
        "description": "Mempelajari kesehatan dan perawatan gigi dan mulut"
    },
    "FT1": {
        "name": "Teknik Mesin",
        "faculty": "Fakultas Teknik",
        "riasec": "RI",
        "description": "Merancang dan mengembangkan sistem mekanik"
    },
    "FT2": {
        "name": "Teknik Kimia",
        "faculty": "Fakultas Teknik",
        "riasec": "IR",
        "description": "Mengembangkan proses kimia industri"
    },
    "FT3": {
        "name": "Teknik Industri",
        "faculty": "Fakultas Teknik",
        "riasec": "ICE",
        "description": "Mengoptimalkan sistem produksi dan manajemen industri"
    },
    "FT4": {
        "name": "Arsitektur",
        "faculty": "Fakultas Teknik",
        "riasec": "ARI",
        "description": "Merancang bangunan dan tata ruang"
    },
    "FT5": {
        "name": "Teknik Sipil",
        "faculty": "Fakultas Teknik",
        "riasec": "RI",
        "description": "Merancang infrastruktur dan konstruksi"
    },
    "FT6": {
        "name": "Teknik Elektro",
        "faculty": "Fakultas Teknik",
        "riasec": "RI",
        "description": "Mengembangkan sistem kelistrikan dan elektronika"
    },
    "FT7": {
        "name": "Teknik Lingkungan",
        "faculty": "Fakultas Teknik",
        "riasec": "RI",
        "description": "Mengelola lingkungan dan pencegahan pencemaran"
    },
    "FMIPA1": {
        "name": "Matematika",
        "faculty": "Fakultas Matematika dan Ilmu Pengetahuan Alam",
        "riasec": "I",
        "description": "Mempelajari konsep matematika murni dan terapan"
    },
    "FMIPA2": {
        "name": "Kimia",
        "faculty": "Fakultas Matematika dan Ilmu Pengetahuan Alam",
        "riasec": "I",
        "description": "Mempelajari struktur dan reaksi zat kimia"
    },
    "FMIPA3": {
        "name": "Biologi",
        "faculty": "Fakultas Matematika dan Ilmu Pengetahuan Alam",
        "riasec": "I",
        "description": "Mempelajari kehidupan organisme dan ekosistem"
    },
    "FMIPA4": {
        "name": "Fisika",
        "faculty": "Fakultas Matematika dan Ilmu Pengetahuan Alam",
        "riasec": "I",
        "description": "Mempelajari fenomena alam dan hukum fisika"
    },
    "FKM1": {
        "name": "Kesehatan Masyarakat",
        "faculty": "Fakultas Kesehatan Masyarakat",
        "riasec": "SI",
        "description": "Mengelola program kesehatan komunitas"
    },
    "FKM2": {
        "name": "Gizi",
        "faculty": "Fakultas Kesehatan Masyarakat",
        "riasec": "IS",
        "description": "Mengatur dan mengevaluasi status gizi masyarakat"
    },
    "FKEP1": {
        "name": "Ilmu Keperawatan",
        "faculty": "Fakultas Keperawatan",
        "riasec": "SI",
        "description": "Memberikan asuhan keperawatan komprehensif"
    },
    "FF1": {
        "name": "Farmasi",
        "faculty": "Fakultas Farmasi",
        "riasec": "ICS",
        "description": "Mengembangkan dan mengelola obat-obatan"
    },
    "FASILKOM1": {
        "name": "Ilmu Komputer",
        "faculty": "Fakultas Ilmu Komputer dan Teknologi Informasi",
        "riasec": "IRC",
        "description": "Mengembangkan perangkat lunak dan sistem komputer"
    },
    "FASILKOM2": {
        "name": "Teknologi Informasi",
        "faculty": "Fakultas Ilmu Komputer dan Teknologi Informasi",
        "riasec": "CRE",
        "description": "Mengelola sistem informasi dan infrastruktur TI"
    },
    "FHUT1": {
        "name": "Kehutanan",
        "faculty": "Fakultas Kehutanan",
        "riasec": "RI",
        "description": "Mengelola hutan dan konservasi alam"
    }
}

QUESTIONS = [
    # Realistic (R) 
    {
        "id": 1,
        "question": "Saya senang bekerja dengan tangan dan alat-alat praktis",
        "dimension": "R",
        "type": "likert"
    },
    {
        "id": 2,
        "question": "Saya lebih suka pekerjaan yang melibatkan aktivitas fisik daripada duduk di meja sepanjang hari",
        "dimension": "R",
        "type": "likert"
    },
    {
        "id": 3,
        "question": "Saya tertarik memperbaiki atau merakit barang-barang elektronik/mekanik",
        "dimension": "R",
        "type": "likert"
    },
    {
        "id": 4,
        "question": "Saya menikmati pekerjaan di luar ruangan lebih dari dalam ruangan",
        "dimension": "R",
        "type": "likert"
    },
    {
        "id": 5,
        "question": "Saya suka mengoperasikan mesin atau peralatan teknis",
        "dimension": "R",
        "type": "likert"
    },
    
    # Investigative (I) 
    {
        "id": 6,
        "question": "Saya senang menganalisis data dan informasi secara mendalam",
        "dimension": "I",
        "type": "likert"
    },
    {
        "id": 7,
        "question": "Saya tertarik melakukan penelitian dan eksperimen",
        "dimension": "I",
        "type": "likert"
    },
    {
        "id": 8,
        "question": "Saya suka memecahkan masalah yang kompleks",
        "dimension": "I",
        "type": "likert"
    },
    {
        "id": 9,
        "question": "Saya senang membaca artikel ilmiah dan jurnal penelitian",
        "dimension": "I",
        "type": "likert"
    },
    {
        "id": 10,
        "question": "Saya tertarik mempelajari teori-teori baru dan konsep abstrak",
        "dimension": "I",
        "type": "likert"
    },
    
    # Artistic (A) 
    {
        "id": 11,
        "question": "Saya senang mengekspresikan kreativitas melalui seni atau desain",
        "dimension": "A",
        "type": "likert"
    },
    {
        "id": 12,
        "question": "Saya tertarik dengan musik, sastra, atau seni visual",
        "dimension": "A",
        "type": "likert"
    },
    {
        "id": 13,
        "question": "Saya suka menciptakan hal-hal baru yang unik dan inovatif",
        "dimension": "A",
        "type": "likert"
    },
    {
        "id": 14,
        "question": "Saya senang bekerja di lingkungan yang fleksibel dan tidak terstruktur",
        "dimension": "A",
        "type": "likert"
    },
    {
        "id": 15,
        "question": "Saya tertarik mempelajari budaya dan tradisi berbagai daerah",
        "dimension": "A",
        "type": "likert"
    },
    
    # Social (S) 
    {
        "id": 16,
        "question": "Saya senang membantu orang lain menyelesaikan masalah mereka",
        "dimension": "S",
        "type": "likert"
    },
    {
        "id": 17,
        "question": "Saya tertarik bekerja dalam bidang kesehatan atau pendidikan",
        "dimension": "S",
        "type": "likert"
    },
    {
        "id": 18,
        "question": "Saya suka bekerja dalam tim dan berkolaborasi dengan orang lain",
        "dimension": "S",
        "type": "likert"
    },
    {
        "id": 19,
        "question": "Saya peduli dengan kesejahteraan masyarakat dan lingkungan sosial",
        "dimension": "S",
        "type": "likert"
    },
    {
        "id": 20,
        "question": "Saya senang mengajar atau melatih orang lain",
        "dimension": "S",
        "type": "likert"
    },
    
    # Enterprising (E) 
    {
        "id": 21,
        "question": "Saya senang memimpin dan mengarahkan orang lain",
        "dimension": "E",
        "type": "likert"
    },
    {
        "id": 22,
        "question": "Saya tertarik menjalankan bisnis atau berwirausaha",
        "dimension": "E",
        "type": "likert"
    },
    {
        "id": 23,
        "question": "Saya suka bernegosiasi dan meyakinkan orang lain",
        "dimension": "E",
        "type": "likert"
    },
    {
        "id": 24,
        "question": "Saya tertarik dengan dunia politik dan kebijakan publik",
        "dimension": "E",
        "type": "likert"
    },
    {
        "id": 25,
        "question": "Saya senang mengambil risiko untuk mencapai tujuan besar",
        "dimension": "E",
        "type": "likert"
    },
    
    # Conventional (C) 
    {
        "id": 26,
        "question": "Saya senang bekerja dengan data, angka, dan sistem yang terorganisir",
        "dimension": "C",
        "type": "likert"
    },
    {
        "id": 27,
        "question": "Saya lebih suka pekerjaan yang memiliki prosedur dan aturan yang jelas",
        "dimension": "C",
        "type": "likert"
    },
    {
        "id": 28,
        "question": "Saya teliti dan akurat dalam menangani detail-detail penting",
        "dimension": "C",
        "type": "likert"
    },
    {
        "id": 29,
        "question": "Saya senang bekerja di lingkungan kantor yang terstruktur",
        "dimension": "C",
        "type": "likert"
    },
    {
        "id": 30,
        "question": "Saya tertarik dengan pekerjaan administrasi dan manajemen dokumen",
        "dimension": "C",
        "type": "likert"
    }
]

LIKERT_OPTIONS = [
    {"value": 1, "label": "Sangat Tidak Setuju"},
    {"value": 2, "label": "Tidak Setuju"},
    {"value": 3, "label": "Netral"},
    {"value": 4, "label": "Setuju"},
    {"value": 5, "label": "Sangat Setuju"}
]

def calculate_riasec_scores(answers):
    riasec_scores = { 'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0 }
    dimension_counts = { 'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0 }

    for question in QUESTIONS:
        dimension = question['dimension']
        dimension_counts[dimension] += 1

        question_answer = next(
            (ans for ans in answers if ans['question_id'] == question['id']),
            None
        )

        if question_answer:
            riasec_scores[dimension] += question_answer['score']

    normalized_scores = {}
    for dim, total in riasec_scores.items():
        normalized_scores[dim] = total / dimension_counts[dim] if dimension_counts[dim] > 0 else 0

    return normalized_scores


def calculate_major_compatibility(riasec_scores):
    recommendations = []
    
    for major_code, major_info in MAJORS_DATA.items():
        riasec_pattern = list(major_info['riasec'])
        compatibility_score = 0
        total_dimensions = len(riasec_pattern)
        
        for dimension in riasec_pattern:
            if dimension in riasec_scores:
                compatibility_score += riasec_scores[dimension]
        
        max_possible_score = total_dimensions * 5  
        compatibility_percentage = (compatibility_score / max_possible_score) * 100
        
        if compatibility_percentage >= 40:
            recommendations.append({
                "major_code": major_code,
                "major_name": major_info['name'],
                "faculty": major_info['faculty'],
                "description": major_info['description'],
                "riasec_pattern": riasec_pattern,
                "compatibility_score": round(compatibility_score, 2),
                "compatibility_percentage": round(compatibility_percentage, 1)
            })
    
    recommendations.sort(key=lambda x: x['compatibility_percentage'], reverse=True)
    
    return recommendations[:10]

@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        
        if not answers:
            return jsonify({
                "success": False,
                "message": "No answers provided"
            }), 400
        
        if len(answers) != 30:
            return jsonify({
                "success": False,
                "message": f"Expected 30 answers, got {len(answers)}"
            }), 400
        
        riasec_scores = calculate_riasec_scores(answers)

        recommendations = calculate_major_compatibility(riasec_scores)
        
        dominant_type = max(riasec_scores, key=riasec_scores.get)
        
        riasec_percentages = {}
        for dimension, score in riasec_scores.items():
            riasec_percentages[dimension] = round((score / 5) * 100, 1)
        
        return jsonify({
            "success": True,
            "riasec_scores": riasec_scores,
            "riasec_percentages": riasec_percentages,
            "dominant_type": dominant_type,
            "recommendations": recommendations,
            "total_questions": len(QUESTIONS),
            "answered_questions": len(answers),
            "assessment_summary": {
                "R": {"name": "Realistic", "score": riasec_percentages.get('R', 0)},
                "I": {"name": "Investigative", "score": riasec_percentages.get('I', 0)},
                "A": {"name": "Artistic", "score": riasec_percentages.get('A', 0)},
                "S": {"name": "Social", "score": riasec_percentages.get('S', 0)},
                "E": {"name": "Enterprising", "score": riasec_percentages.get('E', 0)},
                "C": {"name": "Conventional", "score": riasec_percentages.get('C', 0)}
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error processing request: {str(e)}"
        }), 500

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get all questions for the RIASEC assessment"""
    formatted_questions = []
    
    for question in QUESTIONS:
        formatted_questions.append({
            "id": question['id'],
            "question": question['question'],
            "dimension": question['dimension'],
            "type": question['type'],
            "options": LIKERT_OPTIONS
        })
    
    return jsonify({
        "success": True,
        "questions": formatted_questions,
        "total_questions": len(QUESTIONS)
    })

@app.route('/api/majors', methods=['GET'])
def get_all_majors():
    """Get all available majors with their RIASEC patterns"""
    majors_list = []
    
    for major_code, major_info in MAJORS_DATA.items():
        majors_list.append({
            "major_code": major_code,
            "major_name": major_info['name'],
            "faculty": major_info['faculty'],
            "riasec_pattern": major_info['riasec'],
            "description": major_info['description']
        })
    
    majors_list.sort(key=lambda x: (x['faculty'], x['major_name']))
    
    return jsonify({
        "success": True,
        "majors": majors_list,
        "total_majors": len(majors_list)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)