// Mock environment before requiring the module
const originalEnv = process.env;

describe('groq-helper', () => {
  beforeEach(() => {
    jest.resetModules();
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  describe('module exports', () => {
    test('exports callGroqAPI function', () => {
      process.env.GROQ_API_KEY = 'test-key';
      const groqHelper = require('../groq-helper');
      expect(typeof groqHelper.callGroqAPI).toBe('function');
    });

    test('exports quickAnalyze function', () => {
      process.env.GROQ_API_KEY = 'test-key';
      const groqHelper = require('../groq-helper');
      expect(typeof groqHelper.quickAnalyze).toBe('function');
    });

    test('exports deepAnalyze function', () => {
      process.env.GROQ_API_KEY = 'test-key';
      const groqHelper = require('../groq-helper');
      expect(typeof groqHelper.deepAnalyze).toBe('function');
    });

    test('exports polishText function', () => {
      process.env.GROQ_API_KEY = 'test-key';
      const groqHelper = require('../groq-helper');
      expect(typeof groqHelper.polishText).toBe('function');
    });
  });

  describe('API configuration', () => {
    test('uses default API URL when not specified', () => {
      process.env.GROQ_API_KEY = 'test-key';
      delete process.env.GROQ_API_URL;
      // The module should load without error
      expect(() => require('../groq-helper')).not.toThrow();
    });

    test('uses custom API URL when specified', () => {
      process.env.GROQ_API_KEY = 'test-key';
      process.env.GROQ_API_URL = 'https://custom.api.com';
      expect(() => require('../groq-helper')).not.toThrow();
    });
  });
});
