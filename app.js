let propertiesData = [];

// Load Properties JSON Data
window.onload = function() {
  fetch('properties.json')
    .then(response => response.json())
    .then(data => {
      propertiesData = data;
      renderProperties(propertiesData);
    })
    .catch(error => console.error('Error loading JSON:', error));
};

function renderProperties(data) {
  const container = document.getElementById('propertyContainer');
  container.innerHTML = '';

  if (data.length === 0) {
    container.innerHTML = '<p style="text-align:center; padding:20px;">કોઈ માહિતી મળી નથી (No Property Found)</p>';
    return;
  }

  data.forEach(item => {
    const isUpcoming = item.status === "Upcoming";
    const badgeText = isUpcoming ? "🔴 ઓપન હરાજી" : "🟡 જૂનું ડેટા";
    const badgeClass = isUpcoming ? "badge-upcoming" : "badge-expired";

    const cardHTML = `
      <div class="card">
        <img src="${item.image_url}" class="card-img" alt="Property Image">
        <div class="card-body">
          <span class="badge ${badgeClass}">${badgeText} (${item.year})</span>
          <h2 class="card-title">${item.title_gu}</h2>
          
          <div class="info-item">🆔 <strong>ઓક્શન ID:</strong> ${item.id}</div>
          <div class="info-item">📍 <strong>વિસ્તાર:</strong> ${item.property_area}</div>
          <div class="info-item">🏛️ <strong>બેંક શાખા:</strong> ${item.bank_branch}</div>
          <div class="info-item">💰 <strong>અંદાજિત રકમ:</strong> ${item.price}</div>
          <div class="info-item">📅 <strong>હરાજી તારીખ:</strong> ${item.auction_date}</div>

          <div class="btn-group">
            <button class="btn btn-whatsapp" onclick="shareToWhatsApp('${item.id}')">
              📲 WhatsApp ગ્રુપમાં શેર કરો
            </button>
            <a href="${item.map_link}" target="_blank" class="btn btn-map">
              🗺️ ગૂગલ મેપ (Google Map) જુઓ
            </a>
            ${item.notice_url !== '#' ? `<a href="${item.notice_url}" target="_blank" class="btn btn-pdf">📄 ઓપન નોટિસ PDF</a>` : ''}
          </div>
        </div>
      </div>
    `;
    container.innerHTML += cardHTML;
  });
}

function filterProperties() {
  const searchVal = document.getElementById('searchInput').value.toLowerCase();
  const areaVal = document.getElementById('areaFilter').value;
  const statusVal = document.getElementById('statusFilter').value;

  const filtered = propertiesData.filter(item => {
    const matchesSearch = item.title_gu.toLowerCase().includes(searchVal) || 
                          item.property_area.toLowerCase().includes(searchVal) ||
                          item.bank_branch.toLowerCase().includes(searchVal);

    const matchesArea = (areaVal === 'ALL') || item.property_area.includes(areaVal);
    const matchesStatus = (statusVal === 'ALL') || item.status === statusVal;

    return matchesSearch && matchesArea && matchesStatus;
  });

  renderProperties(filtered);
}

function shareToWhatsApp(id) {
  const item = propertiesData.find(p => p.id === id);
  if (!item) return;

  const appLink = window.location.href;
  const groupLink = "https://chat.whatsapp.com/DJfj7DiGrg0DzegprDfKJU";

  const message = `🚨 *પોરબંદર બેંક હરાજી (Auction) અપડેટ* 🚨\n\n` +
    `🆔 *ઓક્શન ID:* ${item.id}\n` +
    `📌 *મિલકતનું નામ:* ${item.title_gu}\n` +
    `📍 *મિલકતનો વિસ્તાર:* ${item.property_area}\n` +
    `🏛️ *બેંક શાખા:* ${item.bank_branch}\n` +
    `💰 *અંદાજિત રકમ:* ${item.price}\n` +
    `📅 *હરાજીની તારીખ:* ${item.auction_date}\n\n` +
    `🗺️ *ગૂગલ મેપ (Google Map) લોકેશન:*\n${item.map_link}\n\n` +
    `🖼️ *મિલકતનો ફોટો:* ${item.image_url}\n\n` +
    `🔗 *એપ/વેબસાઇટ લિંક:*\n${appLink}\n\n` +
    `📲 *રોજિંદા બેંક ઓક્શન અપડેટ્સ માટે ગ્રુપમાં જોડાઓ:*\n${groupLink}`;

  const fullUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(message)}`;
  window.open(fullUrl, '_blank');
}
