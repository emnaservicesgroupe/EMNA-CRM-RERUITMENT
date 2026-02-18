import React, { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";

const companyInfo = {
  name: "شركة آمنة فيزا سيرفيس",
  description:
    "شركة آمنة فيزا سيرفيس هي شركة متخصصة في تقديم خدمات التوظيف الدولية، تهدف إلى تسهيل عملية توفير فرص العمل للأفراد في الخارج، خاصة في دول مثل رومانيا. تأسست الشركة لتلبية حاجة الأشخاص الذين يسعون للعمل في بيئات مختلفة حول العالم، وتعمل على ربط العمالة المحلية في بلدانهم بالفرص الوظيفية في الخارج، مع التركيز على توفير بيئة عمل آمنة ومستقرة.",
  address: "Avenue Habib Bourguiba, Bardo, Tunisie Tlili Centre 3eme etage",
  socialMedia: {
    facebook: "/emnavisaservices",
    instagram: "@emnavisaservices",
    tiktok: "@emnaservicessltd",
    youtube: "/channel/0029Vat8quJFy72BTZ1zql3s",
  },
};

const jobCategories = [
  "البناء", "التنظيف", "رعاية الأطفال", "رعاية المسنين", "النجارة", "السباكة", "الميكانيكا", "المطاعم"
];

const notifications = [
  "يرجى التقديم لبرنامج B3 في الموعد المحدد.",
  "يجب دفع الجزء المطلوب في خطوة الدفع الثانية.",
  "تم استلام ملفك من قبل مكتب الهجرة والإدارة بنجاح.",
  "يمكنك الآن تنزيل مستند الـ Avis الخاص بك.",
  "تم تحديد موعد لمقابلتك في السفارة، يرجى دفع الجزء المطلوب للحصول على عقد العمل وجميع المستندات.",
];

const workersData = [
  { id: 1, name: "John Doe", skill: "Plumber", location: "New York" },
  { id: 2, name: "Jane Smith", skill: "Electrician", location: "Los Angeles" },
  { id: 3, name: "Mike Johnson", skill: "Carpenter", location: "Chicago" },
];

export default function WorkerList() {
  const [search, setSearch] = useState("");
  const [filteredWorkers, setFilteredWorkers] = useState(workersData);

  useEffect(() => {
    setFilteredWorkers(
      workersData.filter((worker) =>
        worker.name.toLowerCase().includes(search.toLowerCase())
      )
    );
  }, [search]);

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">{companyInfo.name}</h1>
        <p className="text-gray-700">{companyInfo.description}</p>
        <p className="text-gray-500">Address: {companyInfo.address}</p>
        <div className="mt-2">
          <a href={companyInfo.socialMedia.facebook} className="text-blue-500 mr-2">Facebook</a>
          <a href={companyInfo.socialMedia.instagram} className="text-pink-500 mr-2">Instagram</a>
          <a href={companyInfo.socialMedia.tiktok} className="text-red-500 mr-2">TikTok</a>
          <a href={companyInfo.socialMedia.youtube} className="text-red-600">YouTube</a>
        </div>
      </div>
      <div className="mb-6">
        <h2 className="text-xl font-bold">Job Categories</h2>
        <ul className="list-disc pl-6">
          {jobCategories.map((category, index) => (
            <li key={index} className="text-gray-700">{category}</li>
          ))}
        </ul>
      </div>
      <div className="mb-6">
        <h2 className="text-xl font-bold">Notifications</h2>
        <ul className="list-disc pl-6">
          {notifications.map((note, index) => (
            <li key={index} className="text-gray-700">{note}</li>
          ))}
        </ul>
      </div>
      <div className="flex items-center mb-4">
        <Input
          placeholder="Search workers..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="mr-2"
        />
        <Button>
          <Search className="h-4 w-4" />
        </Button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {filteredWorkers.map((worker) => (
          <Card key={worker.id} className="p-4">
            <CardContent>
              <h2 className="text-xl font-semibold">{worker.name}</h2>
              <p className="text-gray-600">{worker.skill}</p>
              <p className="text-gray-500">{worker.location}</p>
            </CardContent>
          </Card>
        ))}
      </div>
      <div className="mt-6">
        <h2 className="text-xl font-bold">Contact Us</h2>
        <Input placeholder="Your Name" className="mb-2" />
        <Input placeholder="Your Email" className="mb-2" />
        <Textarea placeholder="Your Message" className="mb-2" />
        <Button className="mt-2">Send Message</Button>
      </div>
    </div>
  );
}
