# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-06-12

### Added
- Introduced **CUSTOM Game Mode System** with 3 unique new modes:
  
  **ELITE MADNESS**
  - Spawns elite enemies every 15 seconds (3 per wave).
  - Player and elite enemy damage doubled.
  - Recovers max health, energy, and EXP every 10 seconds.
  - Disabled normal enemies and bosses.

  **TINY SPEED DEMON**
  - Player and enemies are smaller and faster.
  - Bullet and boss movement speed increased.
  - Normal enemy spawn every 3s, elite every 10s, boss every 5 minutes.
  - Bosses are active and scaled down in size.

  **DOUBLE BOZOS**
  - Starts with two bosses.
  - No normal or elite enemies.
  - Items drop randomly around the player every second (4 at a time).
  - Increased player health to compensate.
  - Boss waves scale over time with additional sprite skills and cooldowns.

- Added **male and female firing sound effects** to enhance audio feedback.

### Fixed
- Score output now correctly displays on **Game Over** and **Game Won** screens.
- Boss first and second skills now **deal damage when hitting the bottom quarter of the player sprite** as intended.

---