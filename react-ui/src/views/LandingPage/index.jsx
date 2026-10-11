import React from "react";
// Sections
import TopNavbar from "./components/Nav/TopNavbar";
import Header from "./components/Sections/Header";
import Services from "./components/Sections/Services";
import Projects from "./components/Sections/Projects";
import Blog from "./components/Sections/Blog";
import Pricing from "./components/Sections/Pricing";
import Contact from "./components/Sections/Contact";
import Footer from "./components/Sections/Footer";
// Styles
import "./landing.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

export default function LandingPage() {
  return (
    <div className="landing-page">
      <TopNavbar />
      <Header />
      <Services />
      <Projects />
      <Blog />
      <Contact />
      <Footer />
    </div>
  );
}
