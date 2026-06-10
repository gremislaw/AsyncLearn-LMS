import React, { useState, useEffect } from 'react';

function App() {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/courses/')
      .then(res => res.json())
      .then(data => setCourses(data))
      .catch(err => console.error("Error fetching courses:", err));
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>AsyncLearn LMS - Admin Panel</h1>
      <h2>Available Courses</h2>
      <div style={{ display: 'flex', gap: '20px' }}>
        {courses.map(course => (
          <div key={course.id} style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px' }}>
            <h3>{course.title}</h3>
            <p>{course.description}</p>
            <p><strong>Price:</strong> ${course.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
