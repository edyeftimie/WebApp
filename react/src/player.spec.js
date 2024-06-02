import {test, expect} from '@playwright/experimental-ct-react';
import {Player} from './components/player';
import { time } from 'console';

// player.spec.js

// const { test, expect } = require('@playwright/test');

test.describe('Player page', () => {
  let page;

  test.beforeEach(async ({ browser }) => {
    page = await browser.newPage();
    await page.goto('http://localhost:3000/player'); // Adjust URL as needed
  });

  test('renders correctly', async () => {
    const listOfPlayersText = await page.textContent('h2');
    expect(listOfPlayersText).toContain('List of Players');
  });

  test('adds a new player', async () => {
    await page.click('button:has-text("Add Player")');
    await page.fill('input[name="name"]', 'ATest Player');
    await page.fill('input[name="position"]', 'Test Position');
    await page.fill('input[name="club"]', 'Test Club');
    await page.click('button:has-text("Save")');

    await page.waitForSelector('div:has-text("ATest Player")');
    const newPlayerText = await page.textContent('div:has-text("ATest Player")');
    expect(newPlayerText).toContain('ATest Player');
  });

  test('navigates to player details', async () => {
    await page.dblclick('div[role="gridcell"]');
    await page.waitForSelector('h2:has-text("Player Information")');
    const playerInfoHeader = await page.textContent('h2');
    expect(playerInfoHeader).toContain('Player Information');
  });

  test('deletes a player', async () => {
    await page.click('button:has-text("Delete")');
    await page.waitForSelector('div:has-text("ATest Player")', { state: 'detached' , timeout: 500 });
    const deletedPlayerText = await page.textContent('div:has-text("ATest Player")', {timeout: 500}).catch(() => null);
    expect(deletedPlayerText).toBeNull();
  });
});
