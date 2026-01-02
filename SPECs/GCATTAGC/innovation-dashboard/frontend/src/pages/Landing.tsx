import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

export function Landing() {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Innovation Consultancy Dashboard
          </h1>
          <p className="text-xl text-gray-700 mb-8 max-w-2xl mx-auto">
            Guide your clients through the Design Thinking journey: Discovery, Define, Ideate,
            Prototype, and Test. With AI-powered synthesis and dynamic facilitation.
          </p>
          <div className="flex justify-center gap-4">
            <Link
              to="/register"
              className="px-8 py-3 bg-primary-600 text-white text-lg font-medium rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Get Started
            </Link>
            <Link
              to="/login"
              className="px-8 py-3 bg-white text-primary-600 text-lg font-medium rounded-lg border-2 border-primary-600 hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Sign In
            </Link>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-primary-600 text-4xl mb-4">1</div>
            <h3 className="text-xl font-semibold mb-2">Structured Process</h3>
            <p className="text-gray-600">
              Follow the proven Design Thinking methodology with dedicated stages for each phase of
              innovation.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-primary-600 text-4xl mb-4">2</div>
            <h3 className="text-xl font-semibold mb-2">AI-Powered Synthesis</h3>
            <p className="text-gray-600">
              Let AI help synthesize insights, generate summaries, and facilitate the innovation
              process.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-primary-600 text-4xl mb-4">3</div>
            <h3 className="text-xl font-semibold mb-2">Project Management</h3>
            <p className="text-gray-600">
              Manage multiple client projects with ease, track progress, and maintain organized
              documentation.
            </p>
          </div>
        </div>

        <div className="mt-16 bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-3xl font-bold text-center mb-8">Design Thinking Stages</h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              { name: 'Discovery', color: 'blue' },
              { name: 'Define', color: 'purple' },
              { name: 'Ideate', color: 'green' },
              { name: 'Prototype', color: 'orange' },
              { name: 'Test', color: 'red' },
            ].map((stage, index) => (
              <div key={stage.name} className="text-center">
                <div className="text-3xl font-bold text-primary-600 mb-2">{index + 1}</div>
                <div className="text-lg font-semibold">{stage.name}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}


