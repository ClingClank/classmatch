import React, { useState } from "react";
import { useNavigate, Link, Navigate } from "react-router-dom";
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
  FaUser,
  FaEnvelope,
  FaLock,
  FaGraduationCap,
  FaCalendar,
} from "react-icons/fa";
import { useAuth } from "../../context/AuthContext";
import "./Signup.css";

export default function Signup() {
  const navigate = useNavigate();
  const { signup, isAuthenticated } = useAuth();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    major: "",
    year: "Freshman",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Redirect if already authenticated
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await signup(formData);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-page">
      <Container>
        <Row className="justify-content-center py-5">
          <Col md={8} lg={6}>
            <Card className="signup-card shadow-lg border-0">
              <Card.Body className="p-5">
                <div className="text-center mb-4">
                  <div className="signup-icon mb-3">
                    <FaGraduationCap size={50} />
                  </div>
                  <h2 className="text-white mb-2">Join ClassMatch</h2>
                  <p className="text-muted">
                    Create your account to start connecting
                  </p>
                </div>

                {error && (
                  <Alert
                    variant="danger"
                    dismissible
                    onClose={() => setError("")}
                  >
                    {error}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Label className="text-light">Full Name</Form.Label>
                    <div className="input-with-icon">
                      <FaUser className="input-icon" />
                      <Form.Control
                        type="text"
                        name="name"
                        placeholder="John Doe"
                        value={formData.name}
                        onChange={handleChange}
                        required
                        className="ps-5"
                      />
                    </div>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label className="text-light">
                      Email Address
                    </Form.Label>
                    <div className="input-with-icon">
                      <FaEnvelope className="input-icon" />
                      <Form.Control
                        type="email"
                        name="email"
                        placeholder="student@university.edu"
                        value={formData.email}
                        onChange={handleChange}
                        required
                        className="ps-5"
                      />
                    </div>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label className="text-light">Password</Form.Label>
                    <div className="input-with-icon">
                      <FaLock className="input-icon" />
                      <Form.Control
                        type="password"
                        name="password"
                        placeholder="Create a strong password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                        minLength={6}
                        className="ps-5"
                      />
                    </div>
                    <Form.Text className="text-muted">
                      Must be at least 6 characters long
                    </Form.Text>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label className="text-light">Major</Form.Label>
                    <div className="input-with-icon">
                      <FaGraduationCap className="input-icon" />
                      <Form.Control
                        type="text"
                        name="major"
                        placeholder="e.g., Computer Science"
                        value={formData.major}
                        onChange={handleChange}
                        required
                        className="ps-5"
                      />
                    </div>
                  </Form.Group>

                  <Form.Group className="mb-4">
                    <Form.Label className="text-light">
                      Academic Year
                    </Form.Label>
                    <div className="input-with-icon">
                      <FaCalendar className="input-icon" />
                      <Form.Select
                        name="year"
                        value={formData.year}
                        onChange={handleChange}
                        required
                        className="ps-5"
                      >
                        <option value="Freshman">Freshman</option>
                        <option value="Sophomore">Sophomore</option>
                        <option value="Junior">Junior</option>
                        <option value="Senior">Senior</option>
                        <option value="Graduate">Graduate</option>
                      </Form.Select>
                    </div>
                  </Form.Group>

                  <Button
                    variant="primary"
                    type="submit"
                    className="w-100 py-2 mb-3"
                    disabled={loading}
                    size="lg"
                  >
                    {loading ? "Creating Account..." : "Create Account"}
                  </Button>
                </Form>

                <div className="text-center mt-4">
                  <p className="text-muted">
                    Already have an account?{" "}
                    <Link to="/" className="text-primary fw-semibold">
                      Sign In
                    </Link>
                  </p>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
