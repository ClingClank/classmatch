import React, { useState } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  Alert,
} from "react-bootstrap";
import {
  FaUsers,
  FaBook,
  FaClock,
  FaMapMarkerAlt,
  FaHashtag,
} from "react-icons/fa";
import { useAuth } from "../../context/AuthContext";
import { getUserCourses } from "../../data/sampleData";
import "./CreateGroup.css";

export default function CreateGroup() {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    name: "",
    courseId: "",
    description: "",
    meetingTime: "",
    location: "",
    maxMembers: 6,
    tags: "",
  });
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const userCourses = user ? getUserCourses(user.email) : [];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!formData.courseId) {
      setError("Please select a course");
      return;
    }

    // Simulate group creation
    setSuccess(true);
    setTimeout(() => {
      setSuccess(false);
      setFormData({
        name: "",
        courseId: "",
        description: "",
        meetingTime: "",
        location: "",
        maxMembers: 6,
        tags: "",
      });
    }, 3000);
  };

  if (!user) {
    return null; // Protected route will handle redirect
  }

  return (
    <Container className="create-group-page py-4">
      <Row className="justify-content-center">
        <Col md={10} lg={8}>
          <div className="page-header text-center mb-4">
            <div className="header-icon mb-3">
              <FaUsers size={48} />
            </div>
            <h1 className="display-5 fw-bold text-white mb-2">
              Create Study Group
            </h1>
            <p className="text-muted lead">
              Start a new study group and invite classmates to join
            </p>
          </div>

          {success && (
            <Alert
              variant="success"
              dismissible
              onClose={() => setSuccess(false)}
            >
              Study group created successfully! Others can now find and join
              your group.
            </Alert>
          )}

          {error && (
            <Alert variant="danger" dismissible onClose={() => setError("")}>
              {error}
            </Alert>
          )}

          {userCourses.length === 0 ? (
            <Alert variant="warning">
              You need to enroll in courses before creating a study group.
              <Button
                variant="link"
                href="/browse-courses"
                className="p-0 ms-2"
              >
                Browse Courses
              </Button>
            </Alert>
          ) : (
            <Card className="create-group-card shadow-lg">
              <Card.Body className="p-4">
                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-4">
                    <Form.Label className="text-light fw-semibold">
                      <FaUsers className="me-2" />
                      Group Name
                    </Form.Label>
                    <Form.Control
                      type="text"
                      name="name"
                      placeholder="e.g., Data Structures Study Circle"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      size="lg"
                    />
                  </Form.Group>

                  <Form.Group className="mb-4">
                    <Form.Label className="text-light fw-semibold">
                      <FaBook className="me-2" />
                      Course
                    </Form.Label>
                    <Form.Select
                      name="courseId"
                      value={formData.courseId}
                      onChange={handleChange}
                      required
                      size="lg"
                    >
                      <option value="">Select a course...</option>
                      {userCourses.map((course) => (
                        <option key={course.id} value={course.id}>
                          {course.code} - {course.name}
                        </option>
                      ))}
                    </Form.Select>
                  </Form.Group>

                  <Form.Group className="mb-4">
                    <Form.Label className="text-light fw-semibold">
                      Description
                    </Form.Label>
                    <Form.Control
                      as="textarea"
                      name="description"
                      rows={3}
                      placeholder="Describe the purpose and goals of this study group..."
                      value={formData.description}
                      onChange={handleChange}
                      required
                    />
                    <Form.Text className="text-muted">
                      Be specific about what you want to achieve together
                    </Form.Text>
                  </Form.Group>

                  <Row className="mb-4">
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="text-light fw-semibold">
                          <FaClock className="me-2" />
                          Meeting Time
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="meetingTime"
                          placeholder="e.g., Wednesdays 3:00 PM"
                          value={formData.meetingTime}
                          onChange={handleChange}
                          required
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="text-light fw-semibold">
                          <FaMapMarkerAlt className="me-2" />
                          Location
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="location"
                          placeholder="e.g., Library Room 3B or Online"
                          value={formData.location}
                          onChange={handleChange}
                          required
                        />
                      </Form.Group>
                    </Col>
                  </Row>

                  <Row className="mb-4">
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="text-light fw-semibold">
                          Max Members
                        </Form.Label>
                        <Form.Control
                          type="number"
                          name="maxMembers"
                          min="2"
                          max="20"
                          value={formData.maxMembers}
                          onChange={handleChange}
                          required
                        />
                        <Form.Text className="text-muted">
                          Recommended: 4-8 members
                        </Form.Text>
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="text-light fw-semibold">
                          <FaHashtag className="me-2" />
                          Tags (comma-separated)
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="tags"
                          placeholder="e.g., Algorithms, Coding, Weekly"
                          value={formData.tags}
                          onChange={handleChange}
                        />
                      </Form.Group>
                    </Col>
                  </Row>

                  <div className="d-grid gap-2">
                    <Button
                      variant="primary"
                      type="submit"
                      size="lg"
                      className="py-3"
                    >
                      Create Study Group
                    </Button>
                    <Button
                      variant="outline-secondary"
                      type="button"
                      onClick={() => window.history.back()}
                    >
                      Cancel
                    </Button>
                  </div>
                </Form>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
}
