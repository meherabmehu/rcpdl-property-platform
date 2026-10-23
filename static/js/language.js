/* Django owns locale selection; this map covers interface strings outside the
 * explicitly transcribed Bangla frames. Source Bangla in templates takes priority. */
(() => {
  if (document.documentElement.lang !== 'bn') return;
  const words = {
    'Menu':'মেনু','Project 01':'প্রকল্প 01','Project 02':'প্রকল্প 02','Available':'উপলব্ধ',
    'Gallery':'গ্যালারি','A closer look at our projects':'আমাদের প্রকল্পগুলো কাছ থেকে দেখুন',
    'View gallery':'গ্যালারি দেখুন','Home':'হোম','Projects':'প্রকল্প','About':'আমাদের সম্পর্কে','Contact':'যোগাযোগ',
    'Virtual site visit':'ভার্চুয়াল ভিজিট','Explore the land from anywhere.':'যেকোনো স্থান থেকে জমি ঘুরে দেখুন।',
    'See the land before you decide.':'সিদ্ধান্তের আগে জমি দেখে নিন।',
    'Watch video':'ভিডিও দেখুন','Explore 360°':'360° দেখুন','Video':'ভিডিও','360° view':'360° দেখুন',
    'Select project':'প্রকল্প নির্বাচন করুন','View mode':'দেখার ধরন','Back to projects':'প্রকল্প তালিকায় ফিরে যান',
    'Explore the site':'মিডিয়া','About this project':'এই প্রকল্প সম্পর্কে','A closer look at the land.':'জমি কাছ থেকে দেখুন।',
    'Location':'অবস্থান','Approved location pending':'অনুমোদিত অবস্থান নিশ্চিতকরণের অপেক্ষায়',
    'Open location':'অবস্থান দেখুন','Details to confirm':'নিশ্চিত করতে হবে','Ownership details':'মালিকানার তথ্য',
    'Land category / use':'জমির ধরন / ব্যবহার','Other relevant details':'অন্যান্য প্রাসঙ্গিক তথ্য','To be confirmed':'নিশ্চিতকরণের অপেক্ষায়',
    'Sample details':'নমুনা তথ্য','Land size':'জমির আয়তন','Status':'অবস্থা','Illustrative media':'উদাহরণমূলক মিডিয়া',
    'Privacy':'গোপনীয়তা','Website terms':'ওয়েবসাইটের শর্তাবলি','Terms':'শর্তাবলি',
    'On this page':'এই পাতায়','Draft policy · Company review required':'খসড়া নীতি · কোম্পানির পর্যালোচনা প্রয়োজন',
    'This is a draft version for internal review. Content may change after company approval.':'এটি অভ্যন্তরীণ পর্যালোচনার জন্য একটি খসড়া। কোম্পানির অনুমোদনের পর বিষয়বস্তু পরিবর্তন হতে পারে।',
    'Inquiry details':'অনুসন্ধানের তথ্য','AI conversations':'এআই কথোপকথন','Use and access':'ব্যবহার ও প্রবেশাধিকার',
    'Retention':'সংরক্ষণ','Your choices':'আপনার পছন্দ','Privacy contact':'গোপনীয়তা সংক্রান্ত যোগাযোগ',
    'Information and availability':'তথ্য ও প্রাপ্যতা','Inquiries':'অনুসন্ধান',
    'Let’s talk.':'কথা বলুন।','Let’s talk about your next project.':'আপনার আগামী প্রকল্প নিয়ে কথা বলুন।',
    'Company phone':'কোম্পানির ফোন','Office address':'অফিসের ঠিকানা','Pending confirmation':'নিশ্চিতকরণের অপেক্ষায়',
    'Send us an inquiry':'আগ্রহ জানান','Contact our team':'আমাদের সাথে যোগাযোগ করুন',
    'Have a question about our projects?':'আমাদের প্রকল্প সম্পর্কে প্রশ্ন আছে?',
    'Send us a message and we’ll get back to you.':'বার্তা পাঠান, আমরা আপনার সাথে যোগাযোগ করব।',
    'Land. A clearer':'জমি। আরও স্পষ্ট','perspective.':'দৃষ্টিভঙ্গি।','Discover our approach to land and customer service.':'জমি ও গ্রাহকসেবা সম্পর্কে আমাদের দৃষ্টিভঙ্গি জানুন।',
    'Company introduction pending approval.':'কোম্পানির পরিচিতি অনুমোদনের অপেক্ষায়।',
    'Green, open spaces':'সবুজ, উন্মুক্ত স্থান','Growing communities':'বিকাশমান জনপদ','A brighter tomorrow':'একটি উজ্জ্বল আগামী',
    'AI project assistant':'এআই প্রকল্প সহায়ক','Answers use published project information.':'প্রকাশিত প্রকল্পের তথ্যের ভিত্তিতে উত্তর দেওয়া হয়।',
    'An external AI service processes your questions. Avoid personal details.':'একটি বাহ্যিক এআই সেবা আপনার প্রশ্ন প্রক্রিয়া করে। ব্যক্তিগত তথ্য দেবেন না।',
    'Start chat':'কথোপকথন শুরু করুন','Send':'পাঠান','Send an inquiry':'আগ্রহ জানান','Ask AI':'এআই সহায়তা',
    'Contact details are not sent to the AI service.':'যোগাযোগের তথ্য এআই সেবায় পাঠানো হয় না।',
    'Inquiry received':'আপনার বার্তা পেয়েছি','Thank you for your inquiry.':'আপনার আগ্রহের জন্য ধন্যবাদ।',
    'We have received your message.':'আমরা আপনার বার্তা পেয়েছি।','Your submitted number':'আপনার দেওয়া নম্বর',
    'Company contact':'কোম্পানির যোগাযোগ','Back to project':'প্রকল্পে ফিরে যান','Project':'প্রকল্প',
    'Check your phone number.':'আপনার ফোন নম্বর পরীক্ষা করুন।','Enter a valid phone number.':'সঠিক ফোন নম্বর লিখুন।',
    'Select a project.':'একটি প্রকল্প নির্বাচন করুন।','Edit details':'তথ্য সম্পাদনা করুন','Retry':'আবার চেষ্টা করুন',
    'AI assistant is unavailable right now.':'এআই সহায়ক এখন উপলব্ধ নয়।','Please try again later.':'পরে আবার চেষ্টা করুন।',
    'This media could not load.':'এই মিডিয়াটি লোড করা যায়নি।','Retry media':'মিডিয়া আবার লোড করুন',
    'View photos instead':'ছবি দেখুন','Read transcript':'প্রতিলিপি পড়ুন','Fullscreen':'পূর্ণ পর্দা','Exit fullscreen':'পূর্ণ পর্দা থেকে বের হন',
    'Drag to look around':'চারপাশ দেখতে টানুন','Close':'বন্ধ করুন','Return to gallery':'গ্যালারিতে ফিরে যান',
    'Local demonstration — no external AI requests.':'স্থানীয় প্রদর্শনী — বাহ্যিক এআই সেবায় কোনো অনুরোধ পাঠানো হয় না।'
  };
  const translate = node => {
    if (node.nodeType === Node.TEXT_NODE) {
      const original = node.textContent; const text = original.trim();
      const core = text.replace(/^[←→▶♧☏▤▧◌ⓘ🟢\s]+|[→←\s]+$/gu,'').trim();
      if (words[text]) node.textContent = original.replace(text,words[text]);
      else if (words[core]) node.textContent = original.replace(core,words[core]);
    } else if (node.nodeType === Node.ELEMENT_NODE && !['SCRIPT','STYLE','TEXTAREA'].includes(node.tagName)) [...node.childNodes].forEach(translate);
  };
  translate(document.body);
  const observer = new MutationObserver(records => {observer.disconnect(); records.forEach(record => {record.addedNodes.forEach(translate); if (record.type === 'characterData') translate(record.target);}); observe();});
  const observe = () => observer.observe(document.body,{subtree:true,childList:true,characterData:true}); observe();
})();
