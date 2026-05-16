import re
with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_footer = '''<!-- ASUS FOOTER -->
<footer class="asus-footer" style="background-color: #111111; color: #ffffff; padding: 60px 20px;">
    <div class="footer-inner" style="max-width: 1200px; margin: 0 auto;">
        <div class="footer-grid" style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 40px; margin-bottom: 60px;">
            <div class="footer-col" style="flex: 1; min-width: 200px;">
                <h4 style="color: #ffffff; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 20px;">Biz haqimizda</h4>
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <a href="#" style="color: #999999; font-size: 14px; text-decoration: none;">Brend haqida</a>
                    <a href="#" style="color: #999999; font-size: 14px; text-decoration: none;">Yangiliklar</a>
                </div>
            </div>
            <div class="footer-col" style=\"flex: 1; min-width: 200px;\">
                <h4 style="color: #ffffff; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 20px;">Yordam</h4>
                <div style=\"display: flex; flex-direction: column; gap: 12px;\">
                    <a href="{% url 'help_page' %}" style="color: #999999; font-size: 14px; text-decoration: none;">Qo'llab-quvvatlash</a>
                    <a href="{% url 'help_page' %}#warranty" style="color: #999999; font-size: 14px; text-decoration: none;">Kafolat va qaytarish</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom-nav" style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #333333; padding-top: 30px; font-size: 13px; color: #999999;">
            <div>
                <a href="#" style="color: #999999; margin-right: 15px; text-decoration: none;">Maxfiylik siyosati</a>
                <a href="#" style="color: #999999; margin-right: 15px; text-decoration: none;">Foydalanish shartlari</a>
                <span>© {{ site_settings.site_name|default:'NEXUS' }}. Barcha huquqlar himoyalangan.</span>
            </div>
            <div style="color: #ffffff;">O'zbekiston</div>
        </div>
    </div>
</footer>'''

html = re.sub(r'<footer.*?</footer>', new_footer, html, flags=re.DOTALL)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Footer Replaced')
