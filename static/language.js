let translations = {
  "": {
    "Welcome to the Online Land Registry Portal":
      "अनलाइन भूमि दर्ता पोर्टलमा तपाईंलाई स्वागत छ",
    "Transparent Land Records: Build Trust, Build Nepal":
      "पारदर्शी भूमि अभिलेख : बिश्वास बनाउ, नेपाल बनाउ",
    "Create New Land Record": "नयाँ भूमि अभिलेख सिर्जना गर्नुहोस्",
    "Make Land Transaction": "जग्गा कारोबार गर्नुहोस्",
    "View Land Records": "भूमि अभिलेखहरु हेर्नुहोस्",
    "For any inquiries or assistance, please contact us at:":
      "कुनै पनि सोधपुछ वा सहयोगको लागि, कृपया हामीलाई यहाँ सम्पर्क गर्नुहोस्:",
    "Email: info@landregistry.gov.np": "इमेल: info@landregistry.gov.np",
    "Phone: +977-1-2345678": "फोन: +९७७-१-२३४५६७८",
  },
  view_land_records: {},
};

var path = window.location.pathname;

var segments = path.split("/");

var pathname = segments[segments.length - 1];

function setLanguagePreference(language) {
  document.cookie =
    "language=" + language + "; expires=Fri, 31 Dec 9999 23:59:59 GMT";
}

function getLanguagePreference() {
  var language = "en"; // Default language is English
  var cookies = document.cookie.split(";");
  cookies.forEach((cookie) => {
    var cookieParts = cookie.split("=");
    if (cookieParts[0].trim() === "language") {
      language = cookieParts[1];
    }
  });
  return language;
}

function changeLanguage() {
  var currentLanguage = document.documentElement.lang;
  var languageBtn = document.getElementById("languageBtn");
  if (currentLanguage === "en") {
    languageBtn.innerHTML = "English";
    document.documentElement.lang = "ne";
    setLanguagePreference("ne");
    document.body.innerHTML = translateToNepali(document.body.innerHTML);
  } else {
    languageBtn.innerHTML = "नेपाली";
    document.documentElement.lang = "en";
    setLanguagePreference("en");
    location.reload();
  }
}

function translateToNepali(text) {
  let replacements = translations[pathname];
  Object.keys(replacements).forEach((key) => {
    text = text.replace(key, replacements[key]);
  });
  return text;
}

window.onload = function () {
  var preferredLanguage = getLanguagePreference();
  if (preferredLanguage === "ne") {
    changeLanguage();
  }
};
