import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Pagination,
} from "@mui/material";
import { getSubscriptionDetails, cancelSubscription } from "../../api/settingsApi";
import { getPaymentHistory } from "../../api/paymentApi";
import { toast } from "react-toastify";

const SubscriptionManagement = () => {
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState(false);
  const [payments, setPayments] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 10;

  useEffect(() => {
    const fetchSubscription = async () => {
      try {
        const data = await getSubscriptionDetails();
        setSubscription(data);
      } catch (error) {
        toast.error("Failed to load subscription details.");
      } finally {
        setLoading(false);
      }
    };

    const fetchPayments = async (pageNum) => {
      try {
        const paymentData = await getPaymentHistory(pageNum, pageSize);
        setPayments(paymentData.payments);
        setTotalPages(Math.ceil(paymentData.total / pageSize));
      } catch (error) {
        toast.error("Failed to load payment history.");
      }
    };

    fetchSubscription();
    fetchPayments(page);
  }, [page]);

  const handleCancelSubscription = async () => {
    if (!subscription) return;

    setCancelling(true);
    try {
      await cancelSubscription();
      toast.success("Subscription canceled successfully.");
      setSubscription(null);
    } catch (error) {
      toast.error("Failed to cancel subscription.");
    } finally {
      setCancelling(false);
    }
  };

  const formatPrice = (amountInCents, currency = "USD") => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency,
    }).format(amountInCents / 100);
  };

  const getPaymentCardStyle = (status) => {
    switch (status) {
      case "SUCCESS":
      case "PAID":
      case "COMPLETE":
        return { backgroundColor: "rgba(0, 255, 0, 0.2)", borderLeft: "5px solid green" };
      case "PENDING":
        return { backgroundColor: "rgba(255, 255, 0, 0.2)", borderLeft: "5px solid yellow" };
      case "FAILED":
        return { backgroundColor: "rgba(255, 0, 0, 0.2)", borderLeft: "5px solid red" };
      default:
        return { backgroundColor: "rgba(255, 255, 255, 0.1)", borderLeft: "5px solid gray" };
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ color: "white" }}>
        Subscription Management
      </Typography>

      {loading ? (
        <CircularProgress color="primary" />
      ) : subscription ? (
        <>
          <List>
            <ListItem>
              <ListItemText
                primary={<Typography sx={{ color: "white" }}>Current Plan</Typography>}
                secondary={
                  <Typography sx={{ color: "white" }}>
                    {subscription?.subscription_name
                      ? `${subscription.subscription_name} (${formatPrice(subscription.price, subscription.currency)})`
                      : "No active plan"}
                  </Typography>
                }
              />
            </ListItem>

            <ListItem>
              <ListItemText
                primary={<Typography sx={{ color: "white" }}>Renewal Date</Typography>}
                secondary={
                  <Typography sx={{ color: "white" }}>
                    {subscription?.renewal_date
                      ? new Date(subscription.renewal_date).toLocaleDateString()
                      : "No upcoming billing"}
                  </Typography>
                }
              />
            </ListItem>
          </List>

          <Box sx={{ display: "flex", gap: 2, mt: 2 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={() => toast.info("Subscription update overlay coming soon!")}
              sx={{ color: "white" }}
            >
              Update Subscription
            </Button>

            <Button
              variant="contained"
              color="error"
              onClick={handleCancelSubscription}
              disabled={cancelling}
              sx={{ color: "white" }}
            >
              {cancelling ? "Cancelling..." : "Cancel Subscription"}
            </Button>
          </Box>
        </>
      ) : (
        <Typography sx={{ color: "white", mt: 2 }}>You are not subscribed to any plan.</Typography>
      )}

      {/* Payment History */}
      <Typography variant="h6" gutterBottom sx={{ mt: 4, color: "white" }}>
        Payment History
      </Typography>

      {payments.length > 0 ? (
        <>
          <List>
            {payments.map((payment) => (
              <ListItem
                key={payment.id}
                sx={{
                  ...getPaymentCardStyle(payment.status),
                  borderRadius: 2,
                  mb: 1,
                  color: "white",
                }}
              >
                <ListItemText
                  primary={`${formatPrice(payment.amount, payment.currency)} - ${payment.status}`}
                  secondary={`Date: ${
                    payment.renewal_date
                      ? new Date(payment.renewal_date).toLocaleDateString()
                      : "Unknown"
                  } | Transaction ID: ${
                    payment.stripe_payment_id ||
                    payment.google_payment_id ||
                    payment.apple_payment_id ||
                    "N/A"
                  }`}
                  sx={{ color: "white" }}
                />
              </ListItem>
            ))}
          </List>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <Pagination
              count={totalPages}
              page={page}
              onChange={(event, value) => setPage(value)}
              sx={{
                display: "flex",
                justifyContent: "center",
                mt: 2,
                "& .MuiPaginationItem-root": { color: "white" },
              }}
            />
          )}
        </>
      ) : (
        <Typography sx={{ color: "white", mt: 2 }}>No payment history available.</Typography>
      )}
    </Box>
  );
};

export default SubscriptionManagement;
