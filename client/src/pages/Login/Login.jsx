import React, { useState, useEffect } from "react";
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
import { FaGraduationCap, FaEnvelope, FaLock } from "react-icons/fa";
import { useAuth } from "../../context/AuthContext";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Redirect if already authenticated
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <Container>
        <Row className="justify-content-center align-items-center min-vh-90">
          <Col md={10} lg={8}>
            <Row className="g-0 shadow-lg login-container">
              {/* Left Side - Branding */}
              <Col
                md={6}
                className="login-brand d-none d-md-flex flex-column justify-content-center align-items-center text-white p-5"
              >
                <FaGraduationCap size={80} className="mb-4 brand-icon" />
                <h1 className="display-4 fw-bold mb-3">ClassMatch</h1>
                <p className="lead text-center mb-4">
                  Connect with classmates, form study groups, and succeed
                  together
                </p>
                <div className="feature-list text-start w-100">
                  <div className="feature-item mb-3">
                    <span className="feature-icon">✓</span>
                    <span>Find study partners in your courses</span>
                  </div>
                  <div className="feature-item mb-3">
                    <span className="feature-icon">✓</span>
                    <span>Join or create study groups</span>
                  </div>
                  <div className="feature-item">
                    <span className="feature-icon">✓</span>
                    <span>Share schedules and resources</span>
                  </div>
                </div>
              </Col>

              {/* Right Side - Login Form */}
              <Col md={6} className="login-form-side p-5">
                <div className="login-form-container">
                  <h2 className="mb-2 text-white">Welcome Back</h2>
                  <p className="text-muted mb-4">
                    Sign in to continue your learning journey
                  </p>

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
                      <Form.Label className="text-light">
                        Email Address
                      </Form.Label>
                      <div className="input-with-icon">
                        <FaEnvelope className="input-icon" />
                        <Form.Control
                          type="email"
                          placeholder="student@university.edu"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          required
                          className="ps-5"
                        />
                      </div>
                    </Form.Group>

                    <Form.Group className="mb-4">
                      <Form.Label className="text-light">Password</Form.Label>
                      <div className="input-with-icon">
                        <FaLock className="input-icon" />
                        <Form.Control
                          type="password"
                          placeholder="Enter your password"
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          required
                          className="ps-5"
                        />
                      </div>
                    </Form.Group>

                    <Button
                      variant="primary"
                      type="submit"
                      className="w-100 py-2 mb-3"
                      disabled={loading}
                      size="lg"
                    >
                      {loading ? "Signing in..." : "Sign In"}
                    </Button>
                  </Form>

                  <div className="text-center mt-4">
                    <p className="text-muted mb-2">
                      Don't have an account?{" "}
                      <Link to="/signup" className="text-primary fw-semibold">
                        Sign Up
                      </Link>
                    </p>
                    <div className="demo-credentials p-3 mt-3 rounded">
                      <small className="text-muted d-block mb-2">
                        <strong>Demo Credentials:</strong>
                      </small>
                      <small className="text-muted d-block">
                        alice.smith@university.edu
                      </small>
                      <small className="text-muted d-block">password123</small>
                    </div>
                  </div>
                </div>
              </Col>
            </Row>
          </Col>
        </Row>
      </Container>
    </div>
  );
}
