import { test, expect } from "@playwright/test";

// Test data
const meetingTitle = "Team Sync";
const updatedMeetingTitle = "Updated Team Sync";
const meetingAgenda = "Discuss project updates";
const updatedAgenda = "Updated project agenda";
const meetingSummary = "Summary of updates";

test.describe("Meeting Tests", () => {
  test.beforeEach(async ({ page }) => {
    // Authenticate before each test
    await page.goto("/login");
    await page.getByPlaceholder("Email").fill("admin@example.com");
    await page.getByPlaceholder("Password").fill("adminpassword");
    await page.getByRole("button", { name: "Log In" }).click();
    await page.waitForURL("/"); // Adjust if needed
  });

  test("Add Meeting: Required fields validation", async ({ page }) => {
    await page.goto("/meetings/add");
    await page.getByRole("button", { name: "Save" }).click();

    // Assert validation errors
    const titleError = await page.locator("#title + span").textContent();
    expect(titleError).toContain("Title is required");

    const agendaError = await page.locator("#agenda + span").textContent();
    expect(agendaError).toContain("Agenda is required");
  });

  test("Add Meeting: Successful creation", async ({ page }) => {
    await page.goto("/meetings/add");
    await page.getByPlaceholder("Title").fill(meetingTitle);
    await page.getByPlaceholder("Agenda").fill(meetingAgenda);
    await page.getByPlaceholder("Summary").fill(meetingSummary);
    await page.getByRole("button", { name: "Save" }).click();

    // Verify the meeting appears in the list
    const newMeeting = await page.getByText(meetingTitle);
    expect(newMeeting).toBeVisible();
  });

  test("Edit Meeting: Successful update", async ({ page }) => {
    // Go to edit page of the first meeting
    await page.goto("/meetings");
    await page.getByRole("button", { name: "Edit Meeting" }).first().click();

    // Update meeting details
    await page.getByPlaceholder("Title").fill(updatedMeetingTitle);
    await page.getByPlaceholder("Agenda").fill(updatedAgenda);
    await page.getByRole("button", { name: "Save" }).click();

    // Verify the updated meeting details
    const updatedMeeting = await page.getByText(updatedMeetingTitle);
    expect(updatedMeeting).toBeVisible();
  });

  test("Delete Meeting: Successful deletion", async ({ page }) => {
    await page.goto("/meetings");
    const meetingToDelete = await page.getByText(updatedMeetingTitle);

    // Trigger deletion
    await page.getByRole("button", { name: "Delete Meeting" }).first().click();
    await page.getByRole("button", { name: "Confirm" }).click();

    // Verify the meeting no longer exists
    await expect(meetingToDelete).not.toBeVisible();
  });
});
