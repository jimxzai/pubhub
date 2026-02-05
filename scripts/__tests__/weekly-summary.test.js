const {
  getWeekMonday,
  countBookReading,
  calculateWordCount,
  getWeekRange
} = require('../weekly-summary');

describe('weekly-summary', () => {
  describe('getWeekMonday', () => {
    test('returns a Monday (day 1) for any input date', () => {
      const testDate = new Date('2025-12-03T12:00:00Z');
      const monday = getWeekMonday(testDate);
      expect(monday.getDay()).toBe(1); // Monday is day 1
    });

    test('returns the same week Monday for consecutive days', () => {
      const tuesday = new Date('2025-12-02T12:00:00Z');
      const wednesday = new Date('2025-12-03T12:00:00Z');
      const mondayFromTuesday = getWeekMonday(tuesday);
      const mondayFromWednesday = getWeekMonday(wednesday);
      expect(mondayFromTuesday.toISOString().split('T')[0]).toBe(
        mondayFromWednesday.toISOString().split('T')[0]
      );
    });

    test('returns Monday for a Monday date', () => {
      // Create a known Monday
      const knownMonday = new Date('2025-12-01T12:00:00Z');
      const result = getWeekMonday(knownMonday);
      // Should return a Monday
      expect(result.getDay()).toBe(1);
    });

    test('returns previous Monday for a Sunday date', () => {
      const sunday = new Date('2025-12-07T12:00:00Z');
      const monday = getWeekMonday(sunday);
      expect(monday.getDay()).toBe(1);
      // The Monday should be before the Sunday
      expect(monday < sunday).toBe(true);
    });

    test('Monday is within 7 days before the input date', () => {
      const inputDate = new Date('2025-12-06T12:00:00Z');
      const monday = getWeekMonday(inputDate);
      const diffDays = Math.floor((inputDate - monday) / (1000 * 60 * 60 * 24));
      expect(diffDays).toBeGreaterThanOrEqual(0);
      expect(diffDays).toBeLessThan(7);
    });
  });

  describe('countBookReading', () => {
    test('counts Chinese hashtags correctly', () => {
      const notes = [
        { content: '今天读了#孙子兵法，感悟很深' },
        { content: '#资治通鉴 讲述了历史的兴衰' },
        { content: '今日阅读#圣经，思考人生' }
      ];
      const counts = countBookReading(notes);
      expect(counts).toEqual({ sunzi: 1, zizhi: 1, bible: 1 });
    });

    test('counts English hashtags correctly', () => {
      const notes = [
        { content: 'Reading #sunzi today' },
        { content: '#zizhi chronicles' },
        { content: 'Studying #bible passages' }
      ];
      const counts = countBookReading(notes);
      expect(counts).toEqual({ sunzi: 1, zizhi: 1, bible: 1 });
    });

    test('counts multiple books in same note', () => {
      const notes = [
        { content: '#孙子兵法 和 #资治通鉴 对比阅读' },
        { content: '#sunzi #bible combined study' }
      ];
      const counts = countBookReading(notes);
      expect(counts).toEqual({ sunzi: 2, zizhi: 1, bible: 1 });
    });

    test('returns zero counts for notes without book tags', () => {
      const notes = [
        { content: '今天没有读书' },
        { content: 'Random thoughts' }
      ];
      const counts = countBookReading(notes);
      expect(counts).toEqual({ sunzi: 0, zizhi: 0, bible: 0 });
    });

    test('returns zero counts for empty notes array', () => {
      const counts = countBookReading([]);
      expect(counts).toEqual({ sunzi: 0, zizhi: 0, bible: 0 });
    });

    test('handles mixed Chinese and English tags', () => {
      const notes = [
        { content: '#孙子兵法 modern interpretation' },
        { content: '#zizhi history lesson' },
        { content: '#圣经 with #sunzi wisdom' }
      ];
      const counts = countBookReading(notes);
      expect(counts).toEqual({ sunzi: 2, zizhi: 1, bible: 1 });
    });
  });

  describe('calculateWordCount', () => {
    test('calculates word count for simple notes', () => {
      const notes = [
        { content: 'Hello world' },
        { content: 'Another note' }
      ];
      const count = calculateWordCount(notes);
      expect(count).toBe(23); // "Hello world" + "Another note"
    });

    test('removes markdown characters from count', () => {
      const notes = [
        { content: '# Heading\n**bold** text' }
      ];
      const count = calculateWordCount(notes);
      // Original: "# Heading\n**bold** text" -> removes #, *, >
      expect(count).toBeLessThan('# Heading\n**bold** text'.length);
    });

    test('returns zero for empty notes array', () => {
      const count = calculateWordCount([]);
      expect(count).toBe(0);
    });

    test('handles Chinese characters correctly', () => {
      const notes = [
        { content: '今天读书三小时' }
      ];
      const count = calculateWordCount(notes);
      expect(count).toBe(7); // 7 Chinese characters
    });

    test('removes list markers from count', () => {
      const notes = [
        { content: '- Item 1\n- Item 2' }
      ];
      const count = calculateWordCount(notes);
      // "-" characters removed, rest remains
      expect(count).toBe(' Item 1\n Item 2'.length);
    });
  });

  describe('getWeekRange', () => {
    test('returns correct week range format with year and month', () => {
      const date = new Date('2025-12-06T12:00:00Z');
      const range = getWeekRange(date);
      expect(range).toMatch(/^\d{4}-\d{2}-W\d+$/);
      expect(range).toContain('2025');
      expect(range).toContain('-12-');
    });

    test('returns week 1 for days 1-7', () => {
      const date = new Date('2025-12-06T12:00:00Z');
      const range = getWeekRange(date);
      expect(range).toBe('2025-12-W1');
    });

    test('returns week 2 for days 8-14', () => {
      const date = new Date('2025-12-10T12:00:00Z');
      const range = getWeekRange(date);
      expect(range).toBe('2025-12-W2');
    });

    test('returns week 3 for days 15-21', () => {
      const date = new Date('2025-12-18T12:00:00Z');
      const range = getWeekRange(date);
      expect(range).toBe('2025-12-W3');
    });

    test('returns week 5 for end of month', () => {
      const date = new Date('2025-12-31T12:00:00Z');
      const range = getWeekRange(date);
      expect(range).toBe('2025-12-W5');
    });

    test('pads month with zero for single digit months', () => {
      const date = new Date('2025-01-10T12:00:00Z');
      const range = getWeekRange(date);
      expect(range).toContain('-01-');
    });
  });
});
