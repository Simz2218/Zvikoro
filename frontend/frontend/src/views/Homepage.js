import React, { useEffect } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';
import bluesky from "../views/pictures/bluesky.png";

function Homepage() {
  useEffect(() => {
    AOS.init({ duration: 1000 });
  }, []);

  const profiles = [
    {
      name: "Samson Chidzurira",
      title: "District Schools Inspector (DSI)",
      bio: "Oversees all schools in the district, monitors teaching staff, and serves as the Accounting Officer.",
      duties: [
        "Coordinates recruitment, transfers, promotions, and placements",
        "Maintains updated establishment strength",
        "Declares vacancies and endorses interviews"
      ]
    },
    {
      name: "Inspectorate Team",
      title: "Schools Inspectors",
      bio: "Team of four inspectors responsible for school inspections and curriculum implementation.",
      members: ["Mr Bangamuseve J", "Mr Fusirai T", "Mr Chivingira C", "Mr Mucheki V"],
      duties: [
        "Inspect primary and secondary schools",
        "Organize PLAP and ERI workshops",
        "Supervise curriculum rollout and teacher training"
      ]
    },
    {
      name: "Ms Simbo N & Mr Manyuni N",
      title: "Human Resources Department",
      bio: "Manage staffing, grievances, disciplinary cases, allowances, and teacher records.",
      duties: [
        "Process appointments, leave, and terminations",
        "Handle salary queries and misconduct tracking",
        "Maintain teacher data and training records"
      ]
    },
    {
      name: "Mr Manyeruke D & Mrs Chikasha P",
      title: "Accounts Department",
      bio: "Oversee financial records, budgeting, payments, and compliance across district schools.",
      duties: [
        "Produce financial reports and statutory returns",
        "Advise schools on finance policies",
        "Manage SIG and GPE funds"
      ]
    },
    {
      name: "Ms Chidzurira G",
      title: "Administration Department",
      bio: "Handles procurement, transport, maintenance, secretarial services, asset tracking, and office accommodation.",
      duties: [
        "Manage requisitions, stores, and monthly reports",
        "Supervise transport and emergency repairs",
        "Maintain asset and housing records"
      ]
    },
    {
      name: "Mrs Muyambo R",
      title: "Adult Literacy Department",
      bio: "Promotes Non-Formal Education and supervises adult literacy centres and facilitators.",
      duties: [
        "Conduct workshops and collect NFE statistics",
        "Coordinate registration and policy rollout",
        "Support community engagement and reporting"
      ]
    },
    {
      name: "Mr Chitingwiza P",
      title: "Special Needs Education Department",
      bio: "Supports remedial teams, organizes screening, and monitors special needs programmes.",
      duties: [
        "Coordinate early identification and remediation",
        "Liaise with psychologists and trained teachers",
        "Ensure inclusive education practices"
      ]
    }
  ];

  return (
    <div
      style={{
        backgroundImage: `linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url(${bluesky})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        minHeight: '100vh',
        padding: '2rem',
        color: '#fff',
        textShadow: '1px 1px 4px rgba(0,0,0,0.8)',
      }}
    >
      <h1 style={{ fontSize: '2.5rem', textAlign: 'center' }}>
        Better Schools Program Of Zimbabwe
      </h1>
      <h2 style={{ fontSize: '1.5rem', textAlign: 'center', marginBottom: '2rem' }}>
        Zaka District, Masvingo Province
      </h2>

      <p style={{ lineHeight: '1.6', fontSize: '1rem' }} data-aos="fade-up">
        Zaka is a district located 86km southeast of Masvingo under Ndanga communal land. It boasts a strong educational foundation with 94 primary schools and 42 secondary schools, many run by churches and the rural district council. Education was declared a basic human right in 1980, leading to expanded infrastructure and the introduction of science and practical subjects. St Anthony’s High School, now 44 years old, is a nationally renowned institution producing distinguished academics and leaders.
      </p>

      <div data-aos="fade-up" style={{ textAlign: 'center', maxWidth: '900px', margin: '3rem auto' }}>
        <h2>Organisational Vision</h2>
        <p>
          To be the leading provider of inclusive quality Education for Socio-Economic Transformation by 2030.
        </p>

        <h2>Organisational Mission</h2>
        <p>
          To provide equitable, quality, inclusive, relevant and competence-driven Infant Junior and Secondary Education.
        </p>

        <h2>Core Values</h2>
        <p>
          Accountability, Integrity, Transparency, Empathy, Teamwork, and Commitment define the Ministry’s culture and principles.
        </p>

        <h2>Organisational Objectives</h2>
        <p>
          The Ministry aims to provide education for all, improve teaching standards, maintain affordable costs, promote inclusive ECD, strengthen STEM and vocational learning, offer psychological services, coordinate feeding programs, and monitor special needs education.
        </p>
      </div>

      <div style={{ margin: '2rem 0' }} data-aos="zoom-in">
        <iframe
          title="Zaka District Map"
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d379455.2118397272!2d30.930000000000003!3d-20.400000000000002!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1931c3e6e4e2c3f3%3A0x8e3f0f3f0f3f0f3f!2sZaka%2C%20Masvingo%20Province%2C%20Zimbabwe!5e0!3m2!1sen!2szw!4v1692870000000"
          width="100%"
          height="400"
          style={{ border: 0 }}
          allowFullScreen
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
        ></iframe>
      </div>

      <div style={{ marginTop: '3rem' }} data-aos="fade-up">
        <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>District Leadership Profiles</h2>

        {profiles.map((profile, index) => (
          <div key={index} style={{
            background: 'rgba(0,0,0,0.6)',
            padding: '1.5rem',
            borderRadius: '10px',
            marginBottom: '2rem',
            maxWidth: '800px',
            marginLeft: 'auto',
            marginRight: 'auto',
            textAlign: 'center'
          }}>
            <div style={{
              width: '100px',
              height: '100px',
              borderRadius: '50%',
              backgroundColor: '#444',
              margin: '0 auto 1rem'
            }}>
              {/* Replace with <img src={profile.image} /> when ready */}
            </div>
            <h3>{profile.name}</h3>
            <h4 style={{ fontStyle: 'italic', marginBottom: '1rem' }}>{profile.title}</h4>
            <p>{profile.bio}</p>
            {profile.members && (
              <p><strong>Team Members:</strong> {profile.members.join(', ')}</p>
            )}
            <div style={{ marginTop: '1rem', fontSize: '0.95rem' }}>
              {profile.duties.map((duty, i) => (
                <p key={i}>• {duty}</p>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Homepage;
