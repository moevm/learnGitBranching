const CYRILLIC_TO_LATIN = {
  а: 'a', б: 'b', в: 'v', г: 'g', д: 'd', е: 'e', ё: 'e',
  ж: 'zh', з: 'z', и: 'i', й: 'i', к: 'k', л: 'l', м: 'm',
  н: 'n', о: 'o', п: 'p', р: 'r', с: 's', т: 't', у: 'u',
  ф: 'f', х: 'kh', ц: 'ts', ч: 'ch', ш: 'sh', щ: 'shch',
  ъ: '', ы: 'y', ь: '', э: 'e', ю: 'yu', я: 'ya',
};

function transliterate(value) {
  return String(value || '')
    .split('')
    .map((character) => {
      const lowerCharacter = character.toLowerCase();
      const replacement = CYRILLIC_TO_LATIN[lowerCharacter];
      if (replacement === undefined) {
        return character;
      }
      return character === lowerCharacter
        ? replacement
        : replacement.charAt(0).toUpperCase() + replacement.slice(1);
    })
    .join('');
}

function normalizeNamePart(value, fallback) {
  const normalized = transliterate(value)
    .trim()
    .replace(/[^A-Za-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');

  if (!normalized) {
    return fallback;
  }

  return normalized.charAt(0).toUpperCase() + normalized.slice(1);
}

function buildStudentProfile(decoded) {
  const userId = String(decoded.user_id || 'user').replace(/[^A-Za-z0-9]+/g, '');
  const familyName = String(decoded.family_name || '').trim();
  const givenName = String(decoded.given_name || '').trim();
  const fullName = String(
    decoded.full_name || [familyName, givenName].filter(Boolean).join(' '),
  ).trim();

  const familySlug = normalizeNamePart(familyName, 'Student');
  const givenSlug = normalizeNamePart(givenName, userId || 'User');
  const directoryName = `${familySlug}_${givenSlug}_lb3`;

  return {
    userId,
    familyName,
    givenName,
    fullName: fullName || `${familyName} ${givenName}`.trim() || directoryName,
    directoryName,
    branchName: directoryName,
  };
}

function replacePlaceholders(value, profile) {
  if (typeof value === 'string') {
    return value
      .replace(/\{\{STUDENT_DIR\}\}/g, profile.directoryName)
      .replace(/\{\{STUDENT_BRANCH\}\}/g, profile.branchName)
      .replace(/\{\{FULL_NAME\}\}/g, profile.fullName)
      .replace(/\{\{FAMILY_NAME\}\}/g, profile.familyName)
      .replace(/\{\{GIVEN_NAME\}\}/g, profile.givenName);
  }

  if (Array.isArray(value)) {
    return value.map((item) => replacePlaceholders(item, profile));
  }

  if (value && typeof value === 'object') {
    return Object.keys(value).reduce((result, key) => {
      const replacedKey = replacePlaceholders(key, profile);
      result[replacedKey] = replacePlaceholders(value[key], profile);
      return result;
    }, {});
  }

  return value;
}

function personalizeLevel(level, profile) {
  return replacePlaceholders(level, profile);
}

module.exports = {
  buildStudentProfile,
  personalizeLevel,
  transliterate,
};
