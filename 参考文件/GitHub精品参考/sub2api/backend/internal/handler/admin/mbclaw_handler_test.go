package admin

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/require"
)

func TestMBclawHandlerStatus(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := gin.New()
	router.GET("/admin/mbclaw/status", NewMBclawHandler(nil).Status)

	req := httptest.NewRequest(http.MethodGet, "/admin/mbclaw/status", nil)
	w := httptest.NewRecorder()

	router.ServeHTTP(w, req)

	require.Equal(t, http.StatusOK, w.Code)
	require.Contains(t, w.Body.String(), "POST /v1/chat/completions")
	require.Contains(t, w.Body.String(), "POST /api/v1/admin/mbclaw/upstream-tokens")
	require.Contains(t, w.Body.String(), "mbclaw-user-upload")
	require.Contains(t, w.Body.String(), "miclaw-proxy")
	require.Contains(t, w.Body.String(), "account_concurrency")
}
