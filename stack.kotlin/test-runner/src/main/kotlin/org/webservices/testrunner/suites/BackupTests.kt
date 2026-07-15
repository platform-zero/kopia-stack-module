package org.webservices.testrunner.suites

import io.ktor.client.statement.*
import io.ktor.http.*
import org.webservices.testrunner.framework.*

suspend fun TestRunner.backupTests() = suite("Backup Tests") {

    
    test("Kopia server enforces authentication") {
        try {
            val response = client.getRawResponse("${env.endpoints.kopia}/")
            requireAuthBoundary(response, "Kopia unauthenticated UI")
        } catch (e: Exception) {
            fail("Kopia connection failed: ${e.message}")
        }
    }

}
