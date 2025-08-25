import React from 'react';

function Homepage() {
  return (
    <div
      style={{
        backgroundImage: 'url("https://upload.wikimedia.org/wikipedia/commons/6/6a/Flag_of_Zimbabwe.svg")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        minHeight: '100vh',
        padding: '2rem',
        color: '#fff', // white text for contrast
        textShadow: '1px 1px 4px rgba(0,0,0,0.8)', // makes text readable
      }}
    >
      {/* Big Header */}
      <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>
        Better Schools Program Of Zimbabwe
      </h1>

      {/* Smaller Header */}
      <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>
        Zaka District, Masvingo Province
      </h2>

      {/* Paragraph */}
      <p style={{ lineHeight: '1.6', fontSize: '1rem', maxWidth: '900px' }}>
        Masvingo District Better Schools Programme Zimbabwe Centre (BSPZ) in Mucheke,
        which houses the district’s education offices, has been described as the best
        in terms of architectural design. Speaking at the official opening of the centre
        on June 14, 2024, Ministry of Primary and Secondary Education Permanent Secretary
        Moses Mhike said the centre was beautiful and others should have copied from it.
        <br /><br />
        “We were in Zaka on Tuesday and Chivi on Thursday before we came here and we have
        witnessed excellent work in the two districts but Masvingo District has proven to
        be exceptional, we are very proud,” said Mhike.
        <br /><br />
        Mhike said the BSPZ complex was a cornerstone of the National Development Strategy
        1 and 2 and is poised to redefine the education landscape. “BSPZ centres represent
        a strategic investment in human capital development which is a cornerstone of
        National Development Strategy 1 and 2. As a ministry, we envision this space to be
        a hub of creativity, with its state-of-the-art structure, the designed BSPZ centre
        embodies excellence in every facet from its innovative architectural design to its
        cutting-edge facilities. This complex is poised to redefine the education landscape
        of the district,” said Mhike.
        <br /><br />
        He said if the complex was effectively used, it would greatly impact Masvingo Province.
        “The complex has the potential to impact on people’s outcomes across Masvingo Province
        especially when we effectively use it for teacher capacity development,” said Mhike.
        <br /><br />
        Masvingo Provincial Education Director (PED) Shyllate Mhike applauded the District for
        its work and said the province was proud. “I applaud teachers, district personnel and
        school heads who worked together in achieving this goal and as the province, we are
        proud of you Masvingo District,” she said.
        <br /><br />
        The complex comprises a wellness centre, library, computer laboratory, a lecture room
        and kitchens — facets that represent the ministry’s strategic priorities.
      </p>

      {/* Map Embed */}
      <div style={{ margin: '2rem 0' }}>
        <iframe
          title="Zaka Map"
          src="https://www.bing.com/maps?&ty=30&q=Zaka%2C%20Masvingo%20Province%2C%20Zimbabwe&vdpid=8133028753895849985&mb=-20.010049~31.097471~-20.761131~31.7712&cardbg=%23F98745&cp=-20.385513~31.061722&lvl=9.872185"
          width="100%"
          height="400"
          style={{ border: 0 }}
          allowFullScreen
        ></iframe>
      </div>

      {/* Departments Section */}
      <h2 style={{ marginTop: '2rem' }}>Departments & Key Contacts</h2>
      <div style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
        {/* Example: This will later be dynamic from Admin + Users DB */}
        <div style={{ background: 'rgba(0,0,0,0.6)', padding: '1rem', borderRadius: '8px' }}>
          <h3>Samson Chidzurira — DSI Department</h3>
          <p><strong>Bio:</strong> [Bio from linked user profile]</p>
          <p><strong>Contact:</strong> [Phone number from Admin DB]</p>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.6)', padding: '1rem', borderRadius: '8px' }}>
          <h3>Inspectorate Department</h3>
          <p><strong>Bio:</strong> [Bio from linked user profile]</p>
          <p><strong>Contact:</strong> [Phone number from Admin DB]</p>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.6)', padding: '1rem', borderRadius: '8px' }}>
          <h3>Accounts Department</h3>
          <p><strong>Bio:</strong> [Bio from linked user profile]</p>
          <p><strong>Contact:</strong> [Phone number from Admin DB]</p>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.6)', padding: '1rem', borderRadius: '8px' }}>
          <h3>Administration Department</h3>
          <p><strong>Bio:</strong> [Bio from linked user profile]</p>
          <p><strong>Contact:</strong> [Phone number from Admin DB]</p>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.6)', padding: '1rem', borderRadius: '8px' }}>
          <h3>HR Department</h3>
          <p><strong>Bio:</strong> [Bio from linked user profile]</p>
          <p><strong>Contact:</strong> [Phone number from Admin DB]</p>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.6)', padding: '1rem', borderRadius: '8px' }}>
          <h3>IT Department</h3>
          <p><strong>Bio:</strong> [Bio from linked user profile]</p>
          <p><strong>Contact:</strong> [Phone number from Admin DB]</p>
        </div>
      </div>
    </div>
  );
}

export default Homepage;
