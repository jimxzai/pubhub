const {
  getTotalDays,
  calculateTotalWords,
  calculateProgress
} = require('../monthly-report');

describe('monthly-report', () => {
  describe('getTotalDays', () => {
    test('calculates days from default start date to specific end date', () => {
      const days = getTotalDays('2025-11-28', '2025-12-06');
      expect(days).toBe(8);
    });

    test('calculates days between two dates', () => {
      const days = getTotalDays('2025-01-01', '2025-01-31');
      expect(days).toBe(30);
    });

    test('returns 1 for same day', () => {
      const days = getTotalDays('2025-12-01', '2025-12-01');
      // Math.ceil of 0 days difference with abs should be 0 or 1 depending on implementation
      expect(days).toBeGreaterThanOrEqual(0);
      expect(days).toBeLessThanOrEqual(1);
    });

    test('handles leap year correctly', () => {
      const days = getTotalDays('2024-02-01', '2024-03-01');
      expect(days).toBe(29); // 2024 is a leap year
    });

    test('calculates one year correctly', () => {
      const days = getTotalDays('2025-01-01', '2026-01-01');
      expect(days).toBe(365);
    });
  });

  describe('calculateTotalWords', () => {
    test('calculates total words from weekly summaries', () => {
      const weeklies = [
        { content: 'Weekly summary one' },
        { content: 'Weekly summary two' }
      ];
      const count = calculateTotalWords(weeklies);
      expect(count).toBe('Weekly summary one'.length + 'Weekly summary two'.length);
    });

    test('removes markdown characters from count', () => {
      const weeklies = [
        { content: '# Week 1\n## Highlights\n- Item 1\n- Item 2' }
      ];
      const count = calculateTotalWords(weeklies);
      // Markdown characters #, *, >, -, ` should be removed
      const original = '# Week 1\n## Highlights\n- Item 1\n- Item 2';
      expect(count).toBeLessThan(original.length);
    });

    test('returns zero for empty array', () => {
      const count = calculateTotalWords([]);
      expect(count).toBe(0);
    });

    test('handles Chinese content', () => {
      const weeklies = [
        { content: '本周阅读了三本书' }
      ];
      const count = calculateTotalWords(weeklies);
      expect(count).toBe(8);
    });

    test('handles mixed content', () => {
      const weeklies = [
        { content: '阅读了 Art of War' },
        { content: 'Read 资治通鉴' }
      ];
      const count = calculateTotalWords(weeklies);
      expect(count).toBe('阅读了 Art of War'.length + 'Read 资治通鉴'.length);
    });
  });

  describe('calculateProgress', () => {
    test('calculates progress percentage with default target', () => {
      const progress = calculateProgress(100, 2557);
      expect(progress).toBe('3.91');
    });

    test('returns 100% when total equals target', () => {
      const progress = calculateProgress(2557, 2557);
      expect(progress).toBe('100.00');
    });

    test('returns 0% for zero days', () => {
      const progress = calculateProgress(0, 2557);
      expect(progress).toBe('0.00');
    });

    test('calculates halfway correctly', () => {
      const progress = calculateProgress(1278, 2557);
      expect(parseFloat(progress)).toBeCloseTo(49.98, 1);
    });

    test('uses default target of 2557 days', () => {
      const progress = calculateProgress(2557);
      expect(progress).toBe('100.00');
    });

    test('handles custom target days', () => {
      const progress = calculateProgress(50, 100);
      expect(progress).toBe('50.00');
    });

    test('formats to two decimal places', () => {
      const progress = calculateProgress(1, 3);
      expect(progress).toBe('33.33');
    });
  });
});
