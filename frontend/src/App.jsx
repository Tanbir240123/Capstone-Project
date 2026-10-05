import React, { useEffect, useState } from "react";

import {
  Routes,
  Route,
  Link,
  useLocation,
  useNavigate,
  Navigate
} from "react-router-dom";

import {
  uploadFile,
  uploadForecastFile,
  get
} from "./api";

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";


/* =========================================================
   NAVIGATION
========================================================= */

const nav = [
  ["/", "🏠 Dashboard"],
  ["/sales", "📈 Sales Analysis"],
  ["/products", "🏆 Product Analysis"],
  ["/customers", "👥 Customer Analysis"],
  ["/forecast", "🔮 Sales Forecast"],
  ["/performance", "🎯 Business Performance"],

];


const hasAccount = () =>
  !!localStorage.getItem("si_user");


const hasPlan = () =>
  !!localStorage.getItem("si_plan");


/* =========================================================
   ACCESS CONTROL
========================================================= */

function Gate({ children }) {

  if (!hasAccount()) {
    return (
      <Navigate
        to="/create-account"
        replace
      />
    );
  }

  if (!hasPlan()) {
    return (
      <Navigate
        to="/subscription"
        replace
      />
    );
  }

  return children;
}


/* =========================================================
   MAIN LAYOUT
========================================================= */

function Layout({ children }) {

  const loc = useLocation();
  const navg = useNavigate();

  const logout = () => {

    localStorage.clear();

    navg("/create-account");

  };


  return (

    <div className="app">

      <aside>

        <h1>
          SalesInsight
        </h1>

        <p className="muted">
          SME Sales Analytics
        </p>


        {nav.map(([path, name]) => (

          <Link
            key={path}
            to={path}
            className={
              loc.pathname === path
                ? "active"
                : ""
            }
          >
            {name}
          </Link>

        ))}


        <button
          className="logout"
          onClick={logout}
        >
          Log out
        </button>

      </aside>


      <main>
        {children}
      </main>

    </div>
  );
}


/* =========================================================
   PUBLIC LAYOUT
========================================================= */

function Public({ children }) {

  return (

    <div className="public">

      <div className="brand">
        SalesInsight
      </div>

      {children}

    </div>
  );
}


/* =========================================================
   CREATE ACCOUNT
========================================================= */

function CreateAccount() {

  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [err, setErr] = useState("");

  const submit = (e) => {

    e.preventDefault();

    setErr("");

    // Check required fields
    if (
      !name.trim() ||
      !phone.trim() ||
      !email.trim() ||
      !password ||
      !confirmPassword
    ) {
      setErr("Please complete all fields.");
      return;
    }

    // Check phone
    const phoneClean = phone.replace(/\s/g, "");

    if (!/^[0-9+()-]{8,15}$/.test(phoneClean)) {
      setErr("Please enter a valid phone number.");
      return;
    }

    // Check password
    if (password.length < 6) {
      setErr(
        "Password must contain at least 6 characters."
      );
      return;
    }

    // Check password confirmation
    if (password !== confirmPassword) {
      setErr("Passwords do not match.");
      return;
    }

    // Save account information
    localStorage.setItem(
      "si_user",
      JSON.stringify({
        name: name.trim(),
        phone: phone.trim(),
        email: email.trim()
      })
    );

    // Make sure an old plan does not interfere
    localStorage.removeItem("si_plan");

    // Move to subscription page
    window.location.href = "/subscription";
  };


  return (

    <Public>

      <div className="auth card">

        <div className="eyebrow">
          STEP 1 OF 2
        </div>


        <h1>
          Create your SalesInsight account
        </h1>


        <p>
          Set up your account first. You will
          choose a subscription before
          uploading your business dataset.
        </p>


        <form onSubmit={submit}>

          {/* FULL NAME */}

          <label>
            Full name

            <input
              type="text"
              value={name}
              onChange={(e) =>
                setName(e.target.value)
              }
              placeholder="Your full name"
              autoComplete="name"
            />

          </label>


          {/* PHONE */}

          <label>
            Phone number

            <input
              type="tel"
              value={phone}
              onChange={(e) =>
                setPhone(e.target.value)
              }
              placeholder="+61 4XX XXX XXX"
              autoComplete="tel"
            />

          </label>


          {/* EMAIL */}

          <label>
            Email address

            <input
              type="email"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
              placeholder="you@example.com"
              autoComplete="email"
            />

          </label>


          {/* PASSWORD */}

          <label>
            Password

            <input
              type="password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              placeholder="Create a password"
              autoComplete="new-password"
            />

          </label>


          {/* CONFIRM PASSWORD */}

          <label>
            Confirm password

            <input
              type="password"
              value={confirmPassword}
              onChange={(e) =>
                setConfirmPassword(e.target.value)
              }
              placeholder="Confirm your password"
              autoComplete="new-password"
            />

          </label>


          {/* ERROR */}

          {err && (

            <div className="error">
              {err}
            </div>

          )}


          {/* SUBMIT */}

          <button type="submit">
            Create account & continue
          </button>

        </form>

      </div>

    </Public>

  );
}

/* =========================================================
   SUBSCRIPTION
========================================================= */

function Subscription() {
  const nav = useNavigate();

  const plans = [
    {
      id: "trial",
      name: "7-Day Trial",
      price: "$5",
      note: "one-time payment",
      tag: "Limited",
      description:
        "Try SalesInsight for 7 days with limited analytics features.",
      features: [
        "Dashboard overview",
        "Basic sales analysis",
        "Top product analysis",
        "7-day access",
        "Limited forecasting",
      ],
    },
    {
      id: "monthly",
      name: "Monthly",
      price: "$60",
      note: "per month",
      tag: "Popular",
      description: "Full SalesInsight access with monthly billing.",
      features: [
        "Full sales dashboard",
        "Sales analysis",
        "Product analysis",
        "Customer analysis",
        "Sales forecasting",
        "Business performance score",
        "AI-assisted dataset profiling",
      ],
    },
    {
      id: "yearly",
      name: "Yearly",
      price: "$540",
      note: "per year",
      tag: "Best Value",
      description: "Full SalesInsight access with the best annual value.",
      features: [
        "Full sales dashboard",
        "Sales analysis",
        "Product analysis",
        "Customer analysis",
        "Sales forecasting",
        "Business performance score",
        "AI-assisted dataset profiling",
      ],
    },
  ];

  const [selected, setSelected] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("");
  const [step, setStep] = useState("plans");

  const [cardName, setCardName] = useState("");
  const [cardNumber, setCardNumber] = useState("");
  const [expiry, setExpiry] = useState("");
  const [cvv, setCvv] = useState("");

  const [qrCode, setQrCode] = useState("");
  const [paymentReference, setPaymentReference] = useState("");
  const [error, setError] = useState("");

  const selectedPlan = plans.find((plan) => plan.id === selected);

  // ------------------------------------------
  // SELECT PLAN
  // ------------------------------------------

  const choosePlan = (plan) => {
    setSelected(plan.id);
    setPaymentMethod("");
    setError("");
    setStep("payment-method");
  };

  // ------------------------------------------
  // SELECT PAYMENT METHOD
  // ------------------------------------------

  const selectPaymentMethod = async (method) => {
    setPaymentMethod(method);
    setError("");

    if (method === "card") {
      setStep("card");
      return;
    }

    // Apple Pay QR
    const reference = `SI-${Date.now()}-${Math.floor(
      100000 + Math.random() * 900000
    )}`;

    setPaymentReference(reference);

    try {
      const QRCode = await import("qrcode");

      const qrData = [
        "SALESINSIGHT",
        "APPLE_PAY_DEMO",
        `PLAN=${selectedPlan?.name}`,
        `AMOUNT=${selectedPlan?.price}`,
        `REFERENCE=${reference}`,
      ].join("|");

      const generatedQR = await QRCode.toDataURL(qrData, {
        width: 280,
        margin: 2,
        errorCorrectionLevel: "M",
      });

      setQrCode(generatedQR);
      setStep("applepay");
    } catch (err) {
      console.error(err);

      setError(
        "Unable to generate the Apple Pay QR code. Run: npm install qrcode"
      );
    }
  };

  // ------------------------------------------
  // CARD VALIDATION
  // ------------------------------------------

  const processCardPayment = () => {
    setError("");

    const cleanCardNumber = cardNumber.replace(/\s/g, "");

    if (!cardName.trim()) {
      setError("Please enter the cardholder name.");
      return;
    }

    if (!/^\d{16}$/.test(cleanCardNumber)) {
      setError("Please enter a valid 16-digit card number.");
      return;
    }

    if (!/^\d{2}\/\d{2}$/.test(expiry)) {
      setError("Please enter expiry in MM/YY format.");
      return;
    }

    if (!/^\d{3}$/.test(cvv)) {
      setError("Please enter a valid 3-digit CVV.");
      return;
    }

    completePayment("card");
  };

  // ------------------------------------------
  // COMPLETE PAYMENT
  // ------------------------------------------

  const completePayment = (method) => {
    localStorage.setItem("si_plan", selected);

    localStorage.setItem(
      "si_subscription",
      JSON.stringify({
        plan: selected,
        planName: selectedPlan?.name,
        price: selectedPlan?.price,
        paymentMethod: method,
        status: "active",
        activatedAt: new Date().toISOString(),
        paymentReference:
          method === "applepay"
            ? paymentReference
            : `CARD-${Date.now()}`,
      })
    );

    localStorage.removeItem("si_pending_plan");

    setStep("success");

    setTimeout(() => {
      nav("/");
    }, 1200);
  };

  // ------------------------------------------
  // SUCCESS PAGE
  // ------------------------------------------

  if (step === "success") {
    return (
      <div className="page">
        <div className="checkout-card success-card">
          <div className="success-icon">✓</div>

          <h1>Payment Successful</h1>

          <p>
            Your <strong>{selectedPlan?.name}</strong> plan is now active.
          </p>

          <p>Redirecting you to your SalesInsight dashboard...</p>
        </div>
      </div>
    );
  }

  // ------------------------------------------
  // MAIN PAGE
  // ------------------------------------------

  return (
    <div className="page subscription-page">

      {/* HEADER */}

      <div className="subscription-header">

        <button
          className="secondary"
          onClick={() => nav("/")}
          type="button"
        >
          ← Back to Dashboard
        </button>

        <div>
          <h1>Choose Your SalesInsight Plan</h1>

          <p>
            Select a plan and then choose either Card or Apple Pay.
          </p>
        </div>

      </div>

      {/* ======================================
          STEP 1 — PLANS
      ====================================== */}

      {step === "plans" && (
        <div className="plans">

          {plans.map((plan) => (
            <div className="plan" key={plan.id}>

              <div className="plan-tag">
                {plan.tag}
              </div>

              <h2>{plan.name}</h2>

              <div className="plan-price">
                {plan.price}

                <span>
                  {plan.note}
                </span>
              </div>

              <p>
                {plan.description}
              </p>

              <ul>
                {plan.features.map((feature) => (
                  <li key={feature}>
                    ✓ {feature}
                  </li>
                ))}
              </ul>

              <button
                className="primary"
                onClick={() => choosePlan(plan)}
                type="button"
              >
                Choose {plan.name}
              </button>

            </div>
          ))}

        </div>
      )}

      {/* ======================================
          STEP 2 — PAYMENT METHOD
      ====================================== */}

      {step === "payment-method" && selectedPlan && (
        <div className="checkout-card">

          <button
            className="secondary"
            onClick={() => setStep("plans")}
            type="button"
          >
            ← Change Plan
          </button>

          <h2>
            {selectedPlan.name}
          </h2>

          <div className="selected-plan-summary">

            <strong>
              {selectedPlan.price}
            </strong>

            <span>
              {selectedPlan.note}
            </span>

          </div>

          <h3>
            Choose Payment Method
          </h3>

          <div className="payment-options">

            {/* CARD */}

            <button
              className="payment-option"
              onClick={() => selectPaymentMethod("card")}
              type="button"
            >

              <span className="payment-option-icon">
                💳
              </span>

              <span>
                <strong>
                  Credit / Debit Card
                </strong>

                <small>
                  Pay using your card
                </small>
              </span>

            </button>

            {/* APPLE PAY */}

            <button
              className="payment-option"
              onClick={() => selectPaymentMethod("applepay")}
              type="button"
            >

              <span className="payment-option-icon">
                
              </span>

              <span>
                <strong>
                  Apple Pay
                </strong>

                <small>
                  Pay using Apple Pay QR
                </small>
              </span>

            </button>

          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </div>
      )}

      {/* ======================================
          STEP 3 — CARD PAYMENT
      ====================================== */}

      {step === "card" && selectedPlan && (
        <div className="checkout-card">

          <button
            className="secondary"
            onClick={() => setStep("payment-method")}
            type="button"
          >
            ← Change Payment Method
          </button>

          <h2>
            Card Payment
          </h2>

          <p>
            Paying{" "}
            <strong>
              {selectedPlan.price}
            </strong>{" "}
            for{" "}
            <strong>
              {selectedPlan.name}
            </strong>
          </p>

          {/* CARD HOLDER */}

          <div className="form-group">

            <label>
              Cardholder Name
            </label>

            <input
              value={cardName}
              onChange={(e) =>
                setCardName(e.target.value)
              }
              placeholder="John Smith"
            />

          </div>

          {/* CARD NUMBER */}

          <div className="form-group">

            <label>
              Card Number
            </label>

            <input
              value={cardNumber}
              onChange={(e) => {

                const value = e.target.value
                  .replace(/\D/g, "")
                  .slice(0, 16);

                const formatted = value
                  .replace(/(.{4})/g, "$1 ")
                  .trim();

                setCardNumber(formatted);

              }}
              placeholder="1234 5678 9012 3456"
              inputMode="numeric"
            />

          </div>

          {/* EXPIRY + CVV */}

          <div className="card-row">

            <div className="form-group">

              <label>
                Expiry
              </label>

              <input
                value={expiry}
                onChange={(e) => {

                  const value = e.target.value
                    .replace(/\D/g, "")
                    .slice(0, 4);

                  setExpiry(
                    value.length > 2
                      ? `${value.slice(0, 2)}/${value.slice(2)}`
                      : value
                  );

                }}
                placeholder="MM/YY"
                inputMode="numeric"
              />

            </div>

            <div className="form-group">

              <label>
                CVV
              </label>

              <input
                value={cvv}
                onChange={(e) =>
                  setCvv(
                    e.target.value
                      .replace(/\D/g, "")
                      .slice(0, 3)
                  )
                }
                placeholder="123"
                type="password"
                inputMode="numeric"
              />

            </div>

          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          <button
            className="primary"
            onClick={processCardPayment}
            type="button"
          >
            Pay {selectedPlan.price}
          </button>

          <p className="payment-disclaimer">
            Demo checkout. Card details are not stored.
          </p>

        </div>
      )}

      {/* ======================================
          STEP 4 — APPLE PAY
      ====================================== */}

      {step === "applepay" && selectedPlan && (
        <div className="checkout-card applepay-card">

          <button
            className="secondary"
            onClick={() => setStep("payment-method")}
            type="button"
          >
            ← Change Payment Method
          </button>

          <div className="apple-pay-logo">
             Pay
          </div>

          <h2>
            Apple Pay
          </h2>

          <p>
            Scan the QR code below to continue.
          </p>

          {qrCode ? (
            <img
              className="qr-image"
              src={qrCode}
              alt="Apple Pay QR code"
            />
          ) : (
            <div className="qr-loading">
              Generating QR code...
            </div>
          )}

          <div className="qr-payment-details">

            <p>
              <strong>
                Plan:
              </strong>{" "}
              {selectedPlan.name}
            </p>

            <p>
              <strong>
                Amount:
              </strong>{" "}
              {selectedPlan.price}
            </p>

            <p>
              <strong>
                Reference:
              </strong>{" "}
              {paymentReference}
            </p>

          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          {qrCode && (
            <button
              className="primary"
              onClick={() =>
                completePayment("applepay")
              }
              type="button"
            >
              Complete Apple Pay Payment
            </button>
          )}

          <p className="payment-disclaimer">
            Demo Apple Pay flow. A real Apple Pay transaction
            requires a payment gateway integration.
          </p>

        </div>
      )}

    </div>
  );
}


/* =========================================================
   PROCESSING MODAL
========================================================= */

function ProcessingModal() {

  return (

    <div className="processing-overlay">

      <div className="processing-modal">

        <div className="spinner"></div>


        <h3>
          Preparing your Sales Analysis
        </h3>


        <p>
          Please wait while SalesInsight
          processes your dataset.
        </p>

      </div>

    </div>
  );
}


/* =========================================================
   INITIAL DATASET UPLOAD
========================================================= */

function Upload() {

  const [file, setFile] =
    useState(null);

  const [msg, setMsg] =
    useState("");

  const [busy, setBusy] =
    useState(false);

  const navg = useNavigate();


  const submit = async () => {

    if (!file) {

      setMsg(
        "Select a CSV or Excel file first."
      );

      return;
    }


    setBusy(true);
    setMsg("");


    try {

      const response =
        await uploadFile(file);


      localStorage.setItem(
        "dataset_id",
        response.data.dataset_id
      );


      localStorage.setItem(
        "dataset_meta",
        JSON.stringify({

          quality:
            response.data.quality,

          mapping:
            response.data.mapping,

          insights:
            response.data.insights,

          llm_status:
            response.data.llm_status

        })
      );


      /*
        IMPORTANT:

        After the main dataset has finished
        processing, go directly to Sales Analysis.
      */

      navg("/sales");


    } catch (error) {

      setMsg(

        error.response?.data?.detail ||

        error.message ||

        "Unable to process the dataset."

      );

    } finally {

      setBusy(false);

    }

  };


  return (

    <>

      {busy && (
        <ProcessingModal />
      )}


      <div className="uploadbox">

        <div className="upload-icon">
          ↑
        </div>


        <h2>
          Upload your dataset
        </h2>


        <p>
          CSV, XLSX or XLS. The file is
          analyzed first, then cleaned and
          transformed before the analytics
          are calculated.
        </p>


        <input
          id="dataset"
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={(e) => {

            setFile(
              e.target.files?.[0] || null
            );

            setMsg("");

          }}
        />


        <label
          className="filebutton"
          htmlFor="dataset"
        >
          {
            file
              ? file.name
              : "Choose dataset"
          }
        </label>


        <button
          onClick={submit}
          disabled={
            busy || !file
          }
        >
          {
            busy
              ? "Processing…"
              : "Analyse & upload dataset"
          }
        </button>


        {msg && (

          <div className="status">
            {msg}
          </div>

        )}

      </div>

    </>
  );
}


/* =========================================================
   DATASET REQUIRED
========================================================= */

function NeedData() {

  return (

    <div className="card">

      <div className="eyebrow">
        DATASET REQUIRED
      </div>


      <h2>
        Start with your sales dataset
      </h2>


      <p>
        Upload your CSV or Excel file
        to begin using SalesInsight.
      </p>


      <Upload />

    </div>
  );
}


/* =========================================================
   DATA FETCH HOOK
========================================================= */

function useData(path) {

  const [id] = useState(
    () =>
      localStorage.getItem(
        "dataset_id"
      )
  );


  const [d, setD] =
    useState(null);


  const [e, setE] =
    useState("");


  useEffect(() => {

    if (!id) {
      return;
    }


    let cancelled = false;


    get(id, path)

      .then((response) => {

        if (!cancelled) {

          setD(
            response.data
          );

        }

      })

      .catch((error) => {

        if (!cancelled) {

          setE(

            error.response?.data?.detail ||

            error.message ||

            "Unable to load data."

          );

        }

      });


    return () => {

      cancelled = true;

    };

  }, [id, path]);


  return {
    id,
    d,
    e
  };
}


/* =========================================================
   HOME / DASHBOARD
========================================================= */

function Home() {

  const {
    id,
    d,
    e
  } = useData("dashboard");


  if (!id) {

    return (

      <>

        <Header
          title="SalesInsight Dashboard"
          sub="Upload your business dataset to begin"
        />

        <NeedData />

      </>

    );
  }


  if (!d) {

    return (
      <Loading e={e} />
    );

  }


  const meta =
    JSON.parse(
      localStorage.getItem(
        "dataset_meta"
      ) || "{}"
    );


  return (

    <>

      <Header
        title="SalesInsight Dashboard"
        sub="Results calculated from your uploaded dataset"
      />


      <div className="grid6">

        {[
          [
            "Net Sales",
            money(d.sales)
          ],

          [
            "Transactions",
            Number(
              d.transactions || 0
            ).toLocaleString()
          ],

          [
            "Customers",
            Number(
              d.customers || 0
            ).toLocaleString()
          ],

          [
            "Products",
            Number(
              d.products || 0
            ).toLocaleString()
          ],

          [
            "Units",
            num(d.units)
          ],

          [
            "Average Order",
            money(d.aov)
          ]

        ].map((item) => (

          <Kpi
            key={item[0]}
            a={item[0]}
            b={item[1]}
          />

        ))}

      </div>


      <div className="grid2">

        <Card title="Monthly sales">

          <Chart
            data={d.monthly || []}
            x="month"
            y="sales"
          />

        </Card>


        <Card title="Top products by sales">

          <Chart
            data={d.top_products || []}
            x="product"
            y="sales"
            bar
          />

        </Card>

      </div>


      <Card title="AI dataset analysis">

        <p className="muted">

          {
            meta.llm_status ||
            "Dataset profiling completed."
          }

        </p>


        {(meta.insights || [])
          .map((item, index) => (

            <div
              className="insight"
              key={index}
            >
              • {item}
            </div>

          ))}

      </Card>


      <Card title="Data quality and field mapping">

        <div className="quality">

          <span>

            Rows processed:{" "}

            <b>
              {
                meta.quality
                  ?.processed_rows
                  ?.toLocaleString?.() ||
                "—"
              }
            </b>

          </span>


          <span>

            Rows removed:{" "}

            <b>
              {
                meta.quality
                  ?.removed_rows
                  ?.toLocaleString?.() ||
                "—"
              }
            </b>

          </span>


          <span>

            Duplicates:{" "}

            <b>
              {
                meta.quality
                  ?.duplicate_rows
                  ?.toLocaleString?.() ||
                "—"
              }
            </b>

          </span>

        </div>


        <div className="mapping">

          {Object.entries(
            meta.mapping || {}
          )
            .filter(
              ([, value]) =>
                value
            )
            .map(
              ([key, value]) => (

                <span key={key}>

                  <b>
                    {key}
                  </b>

                  {" ← "}

                  {value}

                </span>

              )
            )}

        </div>

      </Card>

    </>
  );
}


/* =========================================================
   SALES ANALYSIS
========================================================= */

function Sales() {

  const {
    id,
    d,
    e
  } = useData("sales");


  if (!id) {
    return <NeedData />;
  }


  if (!d) {
    return <Loading e={e} />;
  }


  return (

    <>

      <Header
        title="Sales Analysis"
      />


      <div className="grid4">

        <Kpi
          a="Net Sales"
          b={money(
            d.kpis?.sales
          )}
        />


        <Kpi
          a="Transactions"
          b={Number(
            d.kpis?.transactions || 0
          ).toLocaleString()}
        />


        <Kpi
          a="Units Sold"
          b={num(
            d.kpis?.units
          )}
        />


        <Kpi
          a="Returns / negative rows"
          b={
            d.kpis?.returns || 0
          }
        />

      </div>


      <Card title="Monthly sales">

        <Chart
          data={d.monthly || []}
          x="month"
          y="sales"
        />

      </Card>


      <div className="grid2">

        <Card title="Daily sales">

          <Chart
            data={d.daily || []}
            x="date"
            y="sales"
          />

        </Card>


        <Card title="Sales by country">

          <Chart
            data={d.country || []}
            x="country"
            y="sales"
            bar
          />

        </Card>

      </div>

    </>
  );
}


/* =========================================================
   PRODUCT ANALYSIS
========================================================= */

function Products() {

  const {
    id,
    d,
    e
  } = useData("products");


  if (!id) {
    return <NeedData />;
  }


  if (!d) {
    return <Loading e={e} />;
  }


  return (

    <>

      <Header
        title="Product Analysis"
      />


      <div className="grid2">

        <Card title="Sales by category">

          <Chart
            data={
              d.categories || []
            }
            x="Category"
            y="sales"
            bar
          />

        </Card>


        <Card title="Top products">

          <Chart
            data={
              (d.products || [])
                .slice(0, 10)
            }
            x="Description"
            y="TotalSales"
            bar
          />

        </Card>

      </div>


      <Table
        rows={
          d.products || []
        }
        cols={[
          "StockCode",
          "Description",
          "Category",
          "TotalQuantity",
          "TotalSales",
          "Transactions"
        ]}
      />

    </>
  );
}


/* =========================================================
   CUSTOMER ANALYSIS
========================================================= */

function Customers() {

  const {
    id,
    d,
    e
  } = useData("customers");


  if (!id) {
    return <NeedData />;
  }


  if (!d) {
    return <Loading e={e} />;
  }


  return (

    <>

      <Header
        title="Customer Analysis"
      />


      <div className="grid2">

        <Card title="Top customers by sales">

          <Chart
            data={
              (d.customers || [])
                .slice(0, 10)
            }
            x="CustomerID"
            y="TotalSales"
            bar
          />

        </Card>


        <Card title="Sales by country">

          <Chart
            data={
              d.countries || []
            }
            x="country"
            y="sales"
            bar
          />

        </Card>

      </div>


      <Table
        rows={
          d.customers || []
        }
        cols={[
          "CustomerID",
          "TotalOrders",
          "TotalQuantity",
          "TotalSales"
        ]}
      />

    </>
  );
}


/* =========================================================
   FORECAST
========================================================= */

function Forecast() {

  const {
    id,
    d,
    e
  } = useData("forecast");


  const [
    forecastData,
    setForecastData
  ] = useState(null);


  const [
    forecastFile,
    setForecastFile
  ] = useState(null);


  const [
    uploading,
    setUploading
  ] = useState(false);


  const [
    forecastError,
    setForecastError
  ] = useState("");


  const handleForecastUpload =
    async (event) => {

      const file =
        event.target.files?.[0];


      if (!file) {
        return;
      }


      setForecastFile(file);

      setForecastError("");

      setUploading(true);


      try {

        const response =
          await uploadForecastFile(
            file
          );


        /*
          IMPORTANT:

          This forecast is stored only
          in React state.

          It does NOT replace the
          original dataset_id.
        */

        setForecastData(
          response.data
        );


      } catch (error) {

        setForecastData(null);


        setForecastError(

          error.response?.data?.detail ||

          error.message ||

          "Unable to generate forecast."

        );


      } finally {

        setUploading(false);

      }

    };


  if (!id) {
    return <NeedData />;
  }


  if (!d) {
    return <Loading e={e} />;
  }


  const displayedForecast =
    forecastData || d;


  return (

    <>

      <Header
        title="Sales Forecast"
        sub="ARIMA forecasting based on historical monthly sales"
      />


      {/* =========================================
          FORECAST FILE UPLOAD
      ========================================= */}

      <Card
        title="Forecast using another dataset"
      >

        <div className="forecast-upload-info">

          <strong>
            For accurate future forecasting,
            upload a minimum of 3 years of
            historical sales data.
          </strong>


          <p>
            This file will only be used
            to recalculate the forecast.
            Your main SalesInsight dataset
            will not be changed.
          </p>


          <input
            id="forecast-file"
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={
              handleForecastUpload
            }
            style={{
              display: "none"
            }}
          />


          <label
            htmlFor="forecast-file"
            className="forecast-upload-button"
          >

            {
              uploading
                ? "Generating forecast…"
                : "Upload Forecast Dataset"
            }

          </label>


          {forecastFile &&
            !forecastError && (

              <p className="forecast-file">

                Using:{" "}

                <strong>
                  {forecastFile.name}
                </strong>

              </p>

            )}


          {forecastError && (

            <div className="forecast-error">

              {forecastError}

            </div>

          )}

        </div>

      </Card>


      {/* =========================================
          FORECAST KPIs
      ========================================= */}

      <div className="grid2">

        <Kpi
          a="Next month forecast"
          b={money(
            displayedForecast
              .next_month
          )}
        />


        <Kpi
          a="3-month forecast total"
          b={money(
            displayedForecast
              .three_month_total
          )}
        />

      </div>


      {/* =========================================
          FORECAST INFORMATION
      ========================================= */}

      {displayedForecast
        .months_used && (

        <Card
          title="Forecast dataset"
        >

          <div className="quality">

            <span>

              Historical months used:{" "}

              <b>
                {
                  displayedForecast
                    .months_used
                }
              </b>

            </span>


            <span>

              Date range:{" "}

              <b>

                {
                  displayedForecast
                    .date_range?.[0]
                }

                {" → "}

                {
                  displayedForecast
                    .date_range?.[1]
                }

              </b>

            </span>

          </div>

        </Card>

      )}


      {/* =========================================
          FORECAST CHART
      ========================================= */}

      <Card title="Forecast">

        <Chart
          data={
            displayedForecast
              .forecast || []
          }
          x="period"
          y="predicted"
        />


        <Table
          rows={
            displayedForecast
              .forecast || []
          }
          cols={[
            "period",
            "predicted",
            "lower",
            "upper"
          ]}
        />

      </Card>

    </>
  );
}


/* =========================================================
   BUSINESS PERFORMANCE
========================================================= */

function Performance() {

  const {
    id,
    d,
    e
  } = useData("performance");


  if (!id) {
    return <NeedData />;
  }


  if (!d) {
    return <Loading e={e} />;
  }


  return (

    <>

      <Header
        title="Business Performance"
      />


      <div className="score">

        {Number(
          d.score || 0
        ).toFixed(1)}

        <small>
          /100
        </small>

      </div>


      <div className="grid4">

        <Kpi
          a="Growth"
          b={`${Number(
            d.growth || 0
          ).toFixed(1)}%`}
        />


        <Kpi
          a="Customers"
          b={d.customers || 0}
        />


        <Kpi
          a="Orders"
          b={d.orders || 0}
        />


        <Kpi
          a="Average Order"
          b={money(d.aov)}
        />

      </div>


      <Card title="Score components">

        <Chart

          data={[
            {
              name: "Growth",
              value:
                d.growth_score || 0
            },

            {
              name: "Customers",
              value:
                d.customer_score || 0
            },

            {
              name: "Order value",
              value:
                d.order_value_score || 0
            },

            {
              name: "Consistency",
              value:
                d.consistency_score || 0
            }

          ]}

          x="name"

          y="value"

          bar

        />

      </Card>

    </>
  );
}


/* =========================================================
   HEADER
========================================================= */

function Header({
  title,
  sub
}) {

  return (

    <header>

      <h2>
        {title}
      </h2>


      {sub && (

        <p>
          {sub}
        </p>

      )}

    </header>
  );
}


/* =========================================================
   KPI
========================================================= */

function Kpi({
  a,
  b
}) {

  return (

    <div className="kpi">

      <span>
        {a}
      </span>


      <strong>
        {b}
      </strong>

    </div>
  );
}


/* =========================================================
   CARD
========================================================= */

function Card({
  title,
  children
}) {

  return (

    <section className="card">

      <h3>
        {title}
      </h3>


      {children}

    </section>
  );
}


/* =========================================================
   CHART
========================================================= */

function Chart({
  data,
  x,
  y,
  bar = false
}) {

  return (

    <div
      style={{
        width: "100%",
        height: 330
      }}
    >

      <ResponsiveContainer>

        {bar ? (

          <BarChart
            data={data || []}
          >

            <XAxis
              dataKey={x}
            />

            <YAxis />

            <Tooltip />

            <Bar
              dataKey={y}
            />

          </BarChart>

        ) : (

          <LineChart
            data={data || []}
          >

            <XAxis
              dataKey={x}
            />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey={y}
              strokeWidth={3}
            />

          </LineChart>

        )}

      </ResponsiveContainer>

    </div>
  );
}


/* =========================================================
   TABLE
========================================================= */

function Table({
  rows,
  cols
}) {

  return (

    <div className="tablewrap">

      <table>

        <thead>

          <tr>

            {cols.map((column) => (

              <th key={column}>
                {column}
              </th>

            ))}

          </tr>

        </thead>


        <tbody>

          {(rows || []).map(
            (row, index) => (

              <tr key={index}>

                {cols.map(
                  (column) => (

                    <td key={column}>

                      {
                        typeof row[column] ===
                        "number"

                          ? row[column]
                              .toLocaleString(
                                undefined,
                                {
                                  maximumFractionDigits: 2
                                }
                              )

                          : row[column]
                      }

                    </td>

                  )
                )}

              </tr>

            )
          )}

        </tbody>

      </table>

    </div>
  );
}


/* =========================================================
   LOADING
========================================================= */

function Loading({
  e
}) {

  return (

    <div className="card">

      <h2>
        {
          e ||
          "Loading analytics…"
        }
      </h2>

    </div>
  );
}


/* =========================================================
   FORMATTING
========================================================= */

function money(value) {

  return `$${Number(
    value || 0
  ).toLocaleString(
    undefined,
    {
      maximumFractionDigits: 2
    }
  )}`;
}


function num(value) {

  return Number(
    value || 0
  ).toLocaleString(
    undefined,
    {
      maximumFractionDigits: 2
    }
  );
}


/* =========================================================
   APPLICATION ROUTES
========================================================= */

export default function App() {

  return (

    <Routes>

      {/* CREATE ACCOUNT */}

      <Route
        path="/create-account"
        element={

          hasAccount() ? (

            <Navigate
              to={
                hasPlan()
                  ? "/"
                  : "/subscription"
              }
              replace
            />

          ) : (

            <CreateAccount />

          )

        }
      />


      {/* SUBSCRIPTION */}

      <Route
        path="/subscription"
        element={

          hasAccount() ? (

            <Subscription />

          ) : (

            <Navigate
              to="/create-account"
              replace
            />

          )

        }
      />


      {/* DASHBOARD */}

      <Route
        path="/"
        element={

          <Gate>

            <Layout>

              <Home />

            </Layout>

          </Gate>

        }
      />


      {/* SALES */}

      <Route
        path="/sales"
        element={

          <Gate>

            <Layout>

              <Sales />

            </Layout>

          </Gate>

        }
      />


      {/* PRODUCTS */}

      <Route
        path="/products"
        element={

          <Gate>

            <Layout>

              <Products />

            </Layout>

          </Gate>

        }
      />


      {/* CUSTOMERS */}

      <Route
        path="/customers"
        element={

          <Gate>

            <Layout>

              <Customers />

            </Layout>

          </Gate>

        }
      />


      {/* FORECAST */}

      <Route
        path="/forecast"
        element={

          <Gate>

            <Layout>

              <Forecast />

            </Layout>

          </Gate>

        }
      />


      {/* PERFORMANCE */}

      <Route
        path="/performance"
        element={

          <Gate>

            <Layout>

              <Performance />

            </Layout>

          </Gate>

        }
      />


      {/* UNKNOWN ROUTE */}

      <Route
        path="*"
        element={
          <Navigate
            to="/"
            replace
          />
        }
      />

    </Routes>
  );
}