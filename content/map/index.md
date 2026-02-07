---
title: Global Map
date: 2025-11-25

type: landing

sections:
  - block: hero
    content:
      title: SEAN Team Around the World
      text: Our team spans across multiple countries in Europe and beyond. Explore the interactive map below to see where our members are based.
    design:
      background:
        gradient_end: '#1976d2'
        gradient_start: '#004ba0'
        text_color_light: true
      
  - block: markdown
    content:
      title: Team Locations Map
      subtitle: ''
      text: |
        <div id="map-container" style="width: 100%; height: 600px; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
          <!-- Map will be rendered here -->
        </div>
        
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

        <script>
          // Initialize map centered on the Atlantic Ocean between Canada and Europe
          const map = L.map('map-container').setView([50, -25], 3);
          
          // Add OpenStreetMap tile layer
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
          }).addTo(map);
          
          // Team members data
          const teamMembers = [
            { name: 'Jean-Michel Bruel', country: 'France', lat: 43.5628, lng: 1.4545, org: 'University of Toulouse' },
            { name: 'Sébastien Mosser', country: 'Canada', lat: 43.2557, lng: -79.8711, org: 'McMaster University' },
            { name: 'Ana Moreira', country: 'Portugal', lat: 38.6597, lng: -9.0156, org: 'NOVA University of Lisbon' },
            { name: 'Antonia Bertolina', country: 'Italy', lat: 42.3631, lng: 13.3972, org: 'Gran Sasso Science Institute' },
            { name: 'Bertrand Meyer', country: 'Switzerland', lat: 47.3769, lng: 8.5472, org: 'Constructor Institute' },
            { name: 'Gilles Perrouin', country: 'Belgium', lat: 50.4501, lng: 4.4699, org: 'University of Namur' },
            { name: 'Jordi Cabot', country: 'Luxembourg', lat: 49.75, lng: 6.16, org: 'Luxembourg Institute of Science and Technology' },
            { name: 'Tanja Vos', country: 'Netherlands', lat: 52.1326, lng: 5.2913, org: 'Open Universiteit' },
            { name: 'Steffen Zschaler', country: 'United Kingdom', lat: 51.5074, lng: -0.1278, org: 'Kings College London' },
            { name: 'Timo Kehrer', country: 'Switzerland', lat: 46.9479, lng: 7.4474, org: 'University of Bern' },
            { name: 'Thomas Riisgaard Hansen', country: 'Denmark', lat: 56.1567, lng: 10.2108, org: 'Digital Research Centre, Denmark' },
            { name: 'Ernest Teniente', country: 'Spain', lat: 41.3851, lng: 2.1734, org: 'Universitat Politècnica de Catalunya' }
          ];
          
          // Country code mapping for easier lookup
          const countryData = {
            'France': { code: 'FR', color: '#FF6B6B' },
            'Canada': { code: 'CA', color: '#4ECDC4' },
            'Portugal': { code: 'PT', color: '#45B7D1' },
            'Italy': { code: 'IT', color: '#96CEB4' },
            'Switzerland': { code: 'CH', color: '#FFEAA7' },
            'Belgium': { code: 'BE', color: '#DDA0DD' },
            'Luxembourg': { code: 'LU', color: '#B19CD9' },
            'Netherlands': { code: 'NL', color: '#FFA500' },
            'Denmark': { code: 'DK', color: '#C0C0C0' },
            'United Kingdom': { code: 'GB', color: '#FFB6C1' },
            'Spain': { code: 'ES', color: '#FF69B4' }
          };
          
          // Country name mapping to handle discrepancies between our names and GeoJSON names
          const countryNameMapping = {
            'United States': 'United States of America',
            'USA': 'United States of America',
            'UK': 'United Kingdom',
            'Russia': 'Russian Federation',
            'Czech Republic': 'Czechia',
            'Macedonia': 'North Macedonia',
            'Swaziland': 'Eswatini',
            'Cape Verde': 'Cabo Verde'
          };
          
          // Function to get the correct country name for GeoJSON
          function getGeoJsonCountryName(countryName) {
            return countryNameMapping[countryName] || countryName;
          }
          
          // Normalize helper for robust country matching
          function normalizeCountryName(name) {
            return (name || '').toLowerCase().trim();
          }

          // Helper to read country identifiers from GeoJSON, regardless of schema variants
          function getFeatureCountryName(feature) {
            const props = feature.properties || {};
            return (
              props.name ||
              props.NAME ||
              props.admin ||
              props.ADMIN ||
              props.name_long ||
              props.NAME_LONG ||
              props.sovereignt ||
              props.SOVEREIGNT ||
              ''
            );
          }

          function getFeatureCountryCode(feature) {
            const props = feature.properties || {};
            return (
              props.iso_a2 ||
              props.ISO_A2 ||
              props.iso_a3 ||
              props.ISO_A3 ||
              ''
            );
          }

          // Index country data by code for quick lookup
          const countryDataByCode = Object.fromEntries(
            Object.entries(countryData).map(([name, info]) => [info.code, { ...info, name }])
          );

          // Create sets of unique member countries (by code and by name)
          const memberCountryCodes = new Set(
            teamMembers.map(m => countryData[m.country]?.code).filter(Boolean)
          );
          const memberCountryNames = new Set(
            teamMembers.map(m => normalizeCountryName(getGeoJsonCountryName(m.country)))
          );
          
          // Debug: Log our member countries
          console.log('Member countries from teamMembers:', Array.from(memberCountryNames));
          
          // Add GeoJSON layer with country highlighting
          fetch('/data/countries.geo.json')
            .then(response => response.json())
            .then(data => {
              // Debug: Log a few sample country names from GeoJSON
              const sampleCountries = data.features.slice(0, 5).map(f => f.properties.name);
              console.log('Sample GeoJSON country names:', sampleCountries);
              
              L.geoJSON(data, {
                style: function(feature) {
                  const featureName = getFeatureCountryName(feature);
                  const featureCode = getFeatureCountryCode(feature);
                  const normalizedFeatureName = normalizeCountryName(featureName);
                  const isMemberCountry =
                    (featureCode && memberCountryCodes.has(featureCode)) ||
                    (normalizedFeatureName && memberCountryNames.has(normalizedFeatureName));
                  // Debug: Log when we find a match
                  if (isMemberCountry) {
                    console.log('Found member match for country:', featureName || featureCode);
                    const color =
                      (featureCode && countryDataByCode[featureCode]?.color) ||
                      countryData[featureName]?.color ||
                      '#90EE90';
                    return {
                      fillColor: color,
                      weight: 2,
                      opacity: 0.8,
                      color: '#333',
                      fillOpacity: 0.5
                    };
                  }
                  return {
                    fillColor: '#e9eef3',
                    weight: 1,
                    opacity: 0.6,
                    color: '#b5c0cc',
                    fillOpacity: 0.25
                  };
                },
                onEachFeature: function(feature, layer) {
                  const featureName = getFeatureCountryName(feature);
                  const featureCode = getFeatureCountryCode(feature);
                  const normalizedFeatureName = normalizeCountryName(featureName);
                  const isMemberCountry =
                    (featureCode && memberCountryCodes.has(featureCode)) ||
                    (normalizedFeatureName && memberCountryNames.has(normalizedFeatureName));
                  if (isMemberCountry) {
                    // Find members by matching country codes first, then fallback to normalized names
                    const members = teamMembers.filter(m => {
                      const memberCode = countryData[m.country]?.code || '';
                      const memberName = normalizeCountryName(getGeoJsonCountryName(m.country));
                      return (
                        (featureCode && memberCode && featureCode === memberCode) ||
                        (normalizedFeatureName && memberName === normalizedFeatureName)
                      );
                    });
                    const membersList = members.map(m => `<li>${m.name}</li>`).join('');
                    layer.bindPopup(`
                      <div style="font-weight: bold; font-size: 1.1em;">${featureName || featureCode}</div>
                      <div style="margin-top: 8px;">
                        <strong>Team Members:</strong>
                        <ul style="margin: 4px 0; padding-left: 20px;">${membersList}</ul>
                      </div>
                    `);
                  }
                }
              }).addTo(map);
            });
          
          // Add markers for each team member
          teamMembers.forEach(member => {
            const marker = L.circleMarker([member.lat, member.lng], {
              radius: 8,
              fillColor: '#1976d2',
              color: '#004ba0',
              weight: 2,
              opacity: 0.9,
              fillOpacity: 0.8
            }).addTo(map);
            
            marker.bindPopup(`
              <div style="font-weight: bold;">${member.name}</div>
              <div style="font-size: 0.9em; color: #666;">${member.country}</div>
              <div style="font-size: 0.85em; color: #999;">${member.org}</div>
            `);
          });
          
          // Add a legend
          const legend = L.control({ position: 'bottomright' });
          legend.onAdd = function() {
            const div = L.DomUtil.create('div', 'info');
            div.style.backgroundColor = 'white';
            div.style.padding = '10px';
            div.style.borderRadius = '4px';
            div.style.boxShadow = '0 0 15px rgba(0,0,0,0.2)';
            div.innerHTML = `
              <div style="font-weight: bold; margin-bottom: 8px;">Legend</div>
              <div style="font-size: 0.9em; margin-bottom: 6px;">
                <span style="display: inline-block; width: 12px; height: 12px; background-color: #1976d2; border-radius: 50%; margin-right: 6px;"></span> Team Member
              </div>
              <div style="font-size: 0.9em; margin-bottom: 6px;">
                <span style="display: inline-block; width: 12px; height: 12px; background-color: #FF6B6B; opacity: 0.4; margin-right: 6px;"></span> Country with Members
              </div>
              <div style="font-size: 0.85em; color: #666; margin-top: 8px;">
                Click markers or countries for details
              </div>
            `;
            return div;
          };
          legend.addTo(map);
        </script>
        
        ## Team Members by Country
        
        | Country | Members |
        |---------|---------|
        | 🇧🇪 Belgium | Gilles Perrouin |
        | 🇨🇦 Canada | Sébastien Mosser |
        | 🇩🇰 Denmark | Thomas Riisgaard Hansen |
        | 🇫🇷 France | Jean-Michel Bruel |
        | 🇮🇹 Italy | Antonia Bertolina |
        | 🇱🇺 Luxembourg | Jordi Cabot |
        | 🇳🇱 Netherlands | Tanja Vos |
        | 🇵🇹 Portugal | Ana Moreira |
        | 🇪🇸 Spain | Ernest Teniente |
        | 🇨🇭 Switzerland | Bertrand Meyer, Timo Kehrer |
        | 🇬🇧 United Kingdom | Steffen Zschaler |

---
