import React, { useState, useEffect } from "react";
import { Container, Row, Col, Form, InputGroup, Alert } from "react-bootstrap";
import { FaSearch } from "react-icons/fa";
import { useAuth } from "../../context/AuthContext";
import CourseCard from "../../components/CourseCard/CourseCard";
import { sampleCourses } from "../../data/sampleData";
import "./BrowseCourses.css";

const BrowseCourses = () => {
  const { user, updateProfile } = useAuth();
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedDepartment, setSelectedDepartment] = useState("All");
  const [filteredCourses, setFilteredCourses] = useState(sampleCourses);
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    let filtered = sampleCourses;

    // Filter by department
    if (selectedDepartment !== "All") {
      filtered = filtered.filter((course) =>
        course.code.startsWith(selectedDepartment)
      );
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(
        (course) =>
          course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          course.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
          course.instructor.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredCourses(filtered);
  }, [searchTerm, selectedDepartment]);

  const handleEnrollCourse = (course) => {
    const currentCourses = user.enrolledCourses || [];
    if (!currentCourses.includes(course.id)) {
      updateProfile({
        enrolledCourses: [...currentCourses, course.id],
      });
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    }
  };

  const departments = ["All", "CS", "MATH"];
  const userEnrolledCourses = user?.enrolledCourses || [];

  return (
    <Container className="browse-courses-page py-4">
      <div className="page-header mb-4">
        <h1 className="display-5 fw-bold text-white mb-2">Browse Courses</h1>
        <p className="text-muted lead">
          Find and join courses to connect with classmates
        </p>
      </div>

      {showSuccess && (
        <Alert
          variant="success"
          dismissible
          onClose={() => setShowSuccess(false)}
        >
          Course added successfully! Check your Dashboard to see matches.
        </Alert>
      )}

      <Row className="mb-4">
        <Col md={8}>
          <InputGroup size="lg">
            <Form.Control
              type="text"
              placeholder="Search by course name, code, or instructor..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </InputGroup>
        </Col>
        <Col md={4}>
          <Form.Select
            size="lg"
            value={selectedDepartment}
            onChange={(e) => setSelectedDepartment(e.target.value)}
            className="department-select"
          >
            {departments.map((dept) => (
              <option key={dept} value={dept}>
                {dept === "All" ? "All Departments" : dept}
              </option>
            ))}
          </Form.Select>
        </Col>
      </Row>

      <div className="results-header mb-3">
        <h5 className="text-light">
          {filteredCourses.length}{" "}
          {filteredCourses.length === 1 ? "Course" : "Courses"} Found
        </h5>
      </div>

      {filteredCourses.length === 0 ? (
        <Alert variant="info">
          No courses found matching your criteria. Try adjusting your search or
          filters.
        </Alert>
      ) : (
        <Row xs={1} md={2} lg={3} className="g-4">
          {filteredCourses.map((course) => (
            <Col key={course.id}>
              <CourseCard
                course={course}
                isEnrolled={userEnrolledCourses.includes(course.id)}
                onEnroll={handleEnrollCourse}
              />
            </Col>
          ))}
        </Row>
      )}
    </Container>
  );
};

export default BrowseCourses;
