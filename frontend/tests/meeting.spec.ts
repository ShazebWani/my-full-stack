import { test as setup, expect } from "@playwright/test";
import { firstSuperuser, firstSuperuserPassword } from "./config";

const authFile = "playwright/.auth/user.json";

setup("authenticate", async ({ page }) => {
  await page.goto("/login");
  await page.waitForSelector('[placeholder="Email"]');
  await page.getByPlaceholder("Email").fill(firstSuperuser);
  await page.getByPlaceholder("Password").fill(firstSuperuserPassword);
  await page.getByRole("button", { name: "Log In" }).click();
  await page.waitForURL("/");
  await page.context().storageState({ path: authFile });
});

setup.describe("Meeting Tests", () => {
  setup.use({ storageState: authFile });

  setup("Add Meeting: Required fields validation", async ({ page }) => {
    await page.goto("/meetings/add");
    await page.waitForSelector('button:has-text("Save")');
    await page.getByRole("button", { name: "Save" }).click();
    const titleError = await page.locator("#title + span").textContent();
    expect(titleError).toContain("Title is required");

    const agendaError = await page.locator("#agenda + span").textContent();
    expect(agendaError).toContain("Agenda is required");
  });

  setup("Add Meeting: Successful submission", async ({ page }) => {
    await page.goto("/meetings/add");
    await page.waitForSelector('[placeholder="Title"]');
    await page.getByPlaceholder("Title").fill("Team Meeting");
    await page.getByPlaceholder("Agenda").fill("Discuss project updates");
    await page.getByPlaceholder("Summary").fill("High-level summary of updates");
    await page.getByRole("button", { name: "Save" }).click();

    await page.waitForSelector(".toast-success");
    const successMessage = await page.locator(".toast-success").textContent();
    expect(successMessage).toContain("Meeting created successfully.");
  });

  setup("Edit Meeting: Required fields validation", async ({ page }) => {
    await page.goto("/meetings/edit/1");
    await page.waitForSelector("#title");
    await page.fill("#title", "");
    await page.getByRole("button", { name: "Save" }).click();
    const titleError = await page.locator("#title + span").textContent();
    expect(titleError).toContain("Title is required");
  });

  setup("Edit Meeting: Successful submission", async ({ page }) => {
    await page.goto("/meetings/edit/1");
    await page.waitForSelector('[placeholder="Title"]');
    await page.getByPlaceholder("Title").fill("Updated Team Meeting");
    await page.getByPlaceholder("Agenda").fill("Updated agenda details");
    await page.getByPlaceholder("Summary").fill("Updated summary details");
    await page.getByRole("button", { name: "Save" }).click();

    await page.waitForSelector(".toast-success");
    const successMessage = await page.locator(".toast-success").textContent();
    expect(successMessage).toContain("Meeting updated successfully.");
  });
});
